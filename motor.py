"""Motor de inferência para o Dr. Byte.

O sistema usa encadeamento para frente: parte das respostas do cliente,
dispara regras compatíveis e propaga conclusões intermediárias até não haver
mais regras novas. Condições negadas só são verdadeiras quando todas as
respostas de entrada que poderiam provar a conclusão negada foram coletadas.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from collections.abc import Mapping, Sequence


PASTA_REGRAS = Path(__file__).with_name("regras")


@dataclass(frozen=True)
class Condicao:
    fato: str
    operador: str = "igual"
    valor: str = "sim"


@dataclass(frozen=True)
class Regra:
    id: str
    sintoma: str
    condicoes: tuple[Condicao, ...]
    conclusao: str
    tipo: str
    acao: str | None
    explicacao: str


def _ler_regras_arquivo(caminho: Path) -> list[Regra]:
    texto = caminho.read_text(encoding="utf-8")
    regras: list[Regra] = []
    # As regras de desliga_sozinho usam blocos cercados por crases; os demais
    # arquivos usam títulos Markdown para separar cada regra.
    blocos_cercados = re.findall(r"```\s*\n(.*?)\n```", texto, flags=re.DOTALL)
    blocos = blocos_cercados or re.split(r"(?=^###\s+[^\n]+)", texto, flags=re.MULTILINE)
    for bloco in blocos:
        id_match = re.search(r"\b((?:NL|SNI|LEN|NC|INT)-R?\d+|DS\d+)\b", bloco)
        se_match = re.search(r"^SE:\s*(.*?)(?=^ENTÃO:)", bloco, re.MULTILINE | re.DOTALL)
        entao_match = re.search(r"^ENTÃO:\s*(.+)$", bloco, re.MULTILINE)
        tipo_match = re.search(r"^TIPO:\s*(intermediária|final)", bloco, re.MULTILINE | re.IGNORECASE)
        explicacao_match = re.search(r"^EXPLICAÇÃO:\s*(.+)$", bloco, re.MULTILINE)
        if not all((id_match, se_match, entao_match, tipo_match, explicacao_match)):
            continue

        condicoes: list[Condicao] = []
        for linha in se_match.group(1).splitlines():
            linha = linha.strip()
            if not linha or linha.upper() == "E":
                continue
            linha = re.sub(r"^E\s+", "", linha, flags=re.IGNORECASE)
            if linha.upper().startswith("NÃO "):
                condicoes.append(Condicao(linha[4:].strip(), "negado"))
            elif "=" in linha:
                fato, valor = (parte.strip() for parte in linha.split("=", 1))
                condicoes.append(Condicao(fato, "igual", valor.casefold()))
            else:
                condicoes.append(Condicao(linha, "verdadeiro"))

        resultado = entao_match.group(1).strip()
        if resultado.startswith("causa ="):
            conclusao = resultado.split("=", 1)[1].strip()
        else:
            conclusao = resultado.split("=", 1)[0].strip()
        acao_match = re.search(r"^AÇÃO:\s*(cliente_resolve|encaminhar_bancada|contacta_provedor)", bloco, re.MULTILINE)
        regras.append(Regra(
            id=id_match.group(1),
            sintoma=caminho.stem,
            condicoes=tuple(condicoes),
            conclusao=conclusao,
            tipo=tipo_match.group(1).casefold(),
            acao=acao_match.group(1) if acao_match else None,
            explicacao=explicacao_match.group(1).strip(),
        ))
    return regras


def carregar_base(pasta: Path = PASTA_REGRAS) -> list[Regra]:
    """Carrega as regras dos Markdown existentes, sem duplicar a base no código."""
    regras: list[Regra] = []
    for arquivo in sorted(pasta.glob("*.md")):
        regras.extend(_ler_regras_arquivo(arquivo))
    return regras


def _entradas_necessarias(conclusao: str, regras: Sequence[Regra], visitados: set[str] | None = None) -> set[str]:
    """Encontra fatos de entrada que podem provar uma conclusão intermediária."""
    visitados = set() if visitados is None else visitados
    if conclusao in visitados:
        return set()
    visitados.add(conclusao)
    entradas: set[str] = set()
    produtores = [r for r in regras if r.tipo == "intermediária" and r.conclusao == conclusao]
    if not produtores:
        # Uma conclusão sem regra produtora é um fato de entrada. A ausência
        # desse fato deve continuar desconhecida, nunca ser tomada por falso.
        return {conclusao}
    for regra in produtores:
        for condicao in regra.condicoes:
            if condicao.operador == "verdadeiro":
                entradas.update(_entradas_necessarias(condicao.fato, regras, visitados.copy()))
            else:
                entradas.add(condicao.fato)
    return entradas


def inferir(
    sintoma: str,
    respostas: Mapping[str, str],
    regras: Sequence[Regra] | None = None,
) -> list[dict[str, str]]:
    """Aplica todas as regras do sintoma e devolve diagnósticos com explicação.

    Chaves ausentes nas respostas são desconhecidas. Isso impede que uma
    condição NÃO seja tratada como verdadeira por simples falta de resposta.
    """
    todas = list(regras if regras is not None else carregar_base())
    aplicaveis = [r for r in todas if r.sintoma == sintoma]
    memoria = {k: str(v).strip().casefold() for k, v in respostas.items()}
    derivados: set[str] = set()
    disparadas: set[str] = set()
    derivacoes: dict[str, list[Regra]] = {}

    # A negação só entra na rodada final, após a saturação das regras positivas.
    positivas = [r for r in aplicaveis if not any(c.operador == "negado" for c in r.condicoes)]
    negadas = [r for r in aplicaveis if r not in positivas]

    def condicao_positiva(condicao: Condicao) -> bool:
        if condicao.operador == "verdadeiro":
            return condicao.fato in derivados
        valor = memoria.get(condicao.fato)
        return valor is not None and valor == condicao.valor

    alterou = True
    while alterou:
        alterou = False
        for regra in positivas:
            if regra.id in disparadas or not all(condicao_positiva(c) for c in regra.condicoes):
                continue
            disparadas.add(regra.id)
            derivacoes.setdefault(regra.conclusao, []).append(regra)
            if regra.tipo == "intermediária" and regra.conclusao not in derivados:
                derivados.add(regra.conclusao)
                alterou = True

    # Uma regra com NÃO X dispara apenas se X não foi derivado e sabemos que
    # todas as entradas usadas pelas regras produtoras de X foram respondidas.
    for regra in negadas:
        valido = True
        for condicao in regra.condicoes:
            if condicao.operador == "negado":
                if condicao.fato in derivados:
                    valido = False
                    break
                if condicao.fato in memoria:
                    if memoria[condicao.fato] != "nao":
                        valido = False
                        break
                    continue
                necessarias = _entradas_necessarias(condicao.fato, aplicaveis)
                if not necessarias.issubset(memoria.keys()) or any(
                    memoria[fato] not in {"sim", "nao", "notebook", "desktop"}
                    for fato in necessarias
                ):
                    valido = False
                    break
            elif not condicao_positiva(condicao):
                valido = False
                break
        if valido:
            disparadas.add(regra.id)
            derivacoes.setdefault(regra.conclusao, []).append(regra)

    def prova_condicao(condicao: Condicao, visitados: set[str] | None = None) -> list[str]:
        visitados = set() if visitados is None else visitados
        if condicao.operador == "negado":
            entradas = sorted(_entradas_necessarias(condicao.fato, aplicaveis))
            respostas_relevantes = ", ".join(f"{f} = {memoria[f]}" for f in entradas if f in memoria)
            if condicao.fato in derivados:
                return [f"{condicao.fato} foi confirmado; portanto, a condição NÃO {condicao.fato} não vale"]
            return [f"NÃO {condicao.fato}: as entradas relevantes foram coletadas ({respostas_relevantes}) e nenhuma regra confirmou {condicao.fato}"]
        if condicao.operador == "verdadeiro":
            if condicao.fato in visitados:
                return [f"{condicao.fato} (conclusão intermediária já detalhada)"]
            visitados.add(condicao.fato)
            explicacoes: list[str] = []
            for produtora in derivacoes.get(condicao.fato, []):
                detalhes = [item for c in produtora.condicoes for item in prova_condicao(c, visitados.copy())]
                explicacoes.append(f"{produtora.id} concluiu {condicao.fato}" + (f" a partir de: {', '.join(detalhes)}" if detalhes else ""))
            return explicacoes or [f"{condicao.fato} foi derivado"]
        valor = memoria.get(condicao.fato, "desconhecido")
        return [f"{condicao.fato} = {valor}"]

    resultados: dict[tuple[str, str], dict[str, str]] = {}
    for regra in aplicaveis:
        if regra.id not in disparadas or regra.tipo != "final" or regra.acao is None:
            continue
        chave = (regra.conclusao, regra.acao)
        if chave not in resultados:
            premissas = [item for condicao in regra.condicoes for item in prova_condicao(condicao)]
            trilha_texto = f"Regra(s): {regra.id}. Premissas: " + "; ".join(premissas) + "."
            resultados[chave] = {
                "causa": regra.conclusao,
                "acao": regra.acao,
                "explicacao": regra.explicacao,
                "regras": regra.id,
                "como": trilha_texto,
                "por_que": regra.explicacao + " " + trilha_texto,
            }
        else:
            atual = resultados[chave]
            atual["regras"] += f", {regra.id}"
            atual["explicacao"] += f" {regra.explicacao}"
            premissas = [item for condicao in regra.condicoes for item in prova_condicao(condicao)]
            atual["como"] += f" Regra(s): {regra.id}. Premissas: " + "; ".join(premissas) + "."
            atual["por_que"] += f" {regra.explicacao} Regra(s): {regra.id}. Premissas: " + "; ".join(premissas) + "."

    ordem_acao = {"encaminhar_bancada": 0, "contacta_provedor": 1, "cliente_resolve": 2}
    return sorted(resultados.values(), key=lambda item: (ordem_acao.get(item["acao"], 9), item["causa"]))


if __name__ == "__main__":
    from interface import executar_interface

    executar_interface(inferir)

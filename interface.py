"""Interface de terminal do Dr. Byte.

Este módulo coleta respostas do cliente e delega a inferência ao motor
implementado separadamente.
"""

from collections.abc import Callable, Mapping, Sequence


PERGUNTAS = {
    "nao_carrega": [
        ("tipo_equipamento", "O equipamento é um notebook ou um computador de mesa?", ("notebook", "desktop")),
        ("carregador_conectado", "O carregador está conectado ao notebook?", ("sim", "nao")),
        ("carregador_conectando_desconectando", "O carregador fica conectando e desconectando sozinho?", ("sim", "nao")),
        ("indicador_carregador_aceso", "A luz indicadora do carregador acende quando ele está na tomada?", ("sim", "nao")),
        ("notebook_indica_carregamento", "O notebook mostra que está carregando quando o carregador é conectado?", ("sim", "nao")),
        ("bateria_aumenta_carga", "A porcentagem da bateria aumenta depois de alguns minutos conectado?", ("sim", "nao")),
        ("tomada_funciona", "Outro aparelho funciona na tomada usada pelo carregador?", ("sim", "nao")),
        ("testou_outra_tomada", "Você testou o carregador em outra tomada?", ("sim", "nao")),
        ("funcionou_outra_tomada", "O carregador funcionou na outra tomada?", ("sim", "nao")),
        ("carregador_ou_cabo_danificado", "O carregador ou o cabo tem cortes, rachaduras, partes expostas ou pinos tortos?", ("sim", "nao")),
    ],
    "internet_nao_conecta": [
        ("tipo_equipamento", "O equipamento é um notebook ou um computador de mesa?", ("notebook", "desktop")),
        ("rede_aparece", "O nome da sua rede aparece na lista de redes disponíveis?", ("sim", "nao")),
        ("outros_dispositivos_conectam", "Outro celular ou computador consegue conectar nessa mesma rede?", ("sim", "nao")),
        ("wifi_ligado", "O Wi-Fi está ligado no equipamento?", ("sim", "nao")),
        ("modo_aviao_ligado", "O modo avião está ligado?", ("sim", "nao")),
        ("cabo_rede_conectado", "O cabo de rede está conectado corretamente ao computador?", ("sim", "nao")),
        ("funciona_com_cabo_rede", "A internet funciona quando o computador é conectado por cabo de rede?", ("sim", "nao")),
        ("reiniciou_roteador", "Você já reiniciou o roteador e esperou alguns minutos?", ("sim", "nao")),
        ("internet_voltou_apos_reiniciar", "A internet voltou depois de reiniciar o roteador?", ("sim", "nao")),
    ],
}

SINTOMAS = {
    "1": ("nao_carrega", "Notebook não carrega"),
    "2": ("internet_nao_conecta", "Internet não conecta"),
}


def ler_opcao(pergunta: str, opcoes: Sequence[str], input_fn: Callable[[str], str] = input) -> str:
    """Lê uma opção válida, repetindo a pergunta quando a entrada for inválida."""
    permitidas = {opcao.casefold(): opcao for opcao in opcoes}
    while True:
        resposta = input_fn(f"{pergunta} ({'/'.join(opcoes)}): ").strip().casefold()
        if resposta in permitidas:
            return permitidas[resposta]
        print(f"Resposta inválida. Digite uma destas opções: {', '.join(opcoes)}.")


def deve_perguntar(fato: str, respostas: Mapping[str, str]) -> bool:
    """Aplica as condições de aplicabilidade das perguntas da interface."""
    if fato == "testou_outra_tomada":
        return respostas.get("tomada_funciona") == "nao"
    if fato == "funcionou_outra_tomada":
        return respostas.get("testou_outra_tomada") == "sim"
    if fato == "internet_voltou_apos_reiniciar":
        return respostas.get("reiniciou_roteador") == "sim"
    return True


def coletar_respostas(sintoma: str, input_fn: Callable[[str], str] = input) -> dict[str, str]:
    """Coleta somente as respostas aplicáveis ao sintoma escolhido."""
    if sintoma not in PERGUNTAS:
        raise ValueError(f"Sintoma sem questionário cadastrado: {sintoma}")

    respostas: dict[str, str] = {}
    for fato, pergunta, opcoes in PERGUNTAS[sintoma]:
        if deve_perguntar(fato, respostas):
            respostas[fato] = ler_opcao(pergunta, opcoes, input_fn)
    return respostas


def exibir_resultados(resultados: Sequence[Mapping[str, str]]) -> None:
    """Exibe diagnósticos e explicações ou informa quando não houve conclusão."""
    if not resultados:
        print("\nNão foi possível concluir com as informações fornecidas.")
        print("Procure a ByteFix para uma avaliação técnica.")
        return

    print("\nDiagnóstico(s) provável(is):")
    for indice, resultado in enumerate(resultados, start=1):
        causa = resultado.get("causa", "não identificado")
        acao = resultado.get("acao", "encaminhar_bancada")
        explicacao = resultado.get("explicacao", "Não há explicação registrada.")
        print(f"\n{indice}. Causa: {causa}")
        print(f"   Ação: {acao}")
        print(f"   Como chegamos a essa conclusão: {explicacao}")


def escolher_sintoma(input_fn: Callable[[str], str] = input) -> str:
    """Exibe o menu e retorna o identificador do sintoma selecionado."""
    print("\nQual problema o equipamento apresenta?")
    for numero, (_, descricao) in SINTOMAS.items():
        print(f"{numero} - {descricao}")
    numero = ler_opcao("Escolha o número", tuple(SINTOMAS), input_fn)
    return SINTOMAS[numero][0]


def executar_interface(
    inferir: Callable[[str, Mapping[str, str]], Sequence[Mapping[str, str]]],
    input_fn: Callable[[str], str] = input,
) -> None:
    """Executa o fluxo da interface usando a função de inferência recebida."""
    print("=== Dr. Byte — Pré-triagem ByteFix ===")
    sintoma = escolher_sintoma(input_fn)
    respostas = coletar_respostas(sintoma, input_fn)
    resultados = inferir(sintoma, respostas)
    exibir_resultados(resultados)


if __name__ == "__main__":
    print("A interface aguarda a integração com o motor de inferência.")

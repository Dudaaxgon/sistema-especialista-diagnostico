"""Interface de terminal do Dr. Byte.

Este módulo coleta respostas do cliente e delega a inferência ao motor
implementado separadamente.
"""

from collections.abc import Callable, Mapping, Sequence


PERGUNTAS = {
    "nao_liga": [
        ("tipo_equipamento", "O equipamento é um notebook ou um computador de mesa?", ("notebook", "desktop")),
        ("sinal_de_vida", "Ao apertar o botão, alguma luz acende ou algum ventilador gira?", ("sim", "nao")),
        ("cabo_energia_conectado", "O cabo de energia está encaixado na entrada do computador?", ("sim", "nao")),
        ("tomada_funciona", "Outro aparelho funciona na tomada usada pelo computador?", ("sim", "nao")),
        ("testou_outra_tomada", "Você testou o computador em outra tomada?", ("sim", "nao")),
        ("funcionou_outra_tomada", "O computador ligou nessa outra tomada?", ("sim", "nao")),
        ("chave_fonte_ligada", "No desktop, a chave atrás do gabinete está na posição I?", ("sim", "nao")),
        ("usa_filtro_linha", "O computador está ligado a um filtro de linha?", ("sim", "nao")),
        ("filtro_linha_ligado", "O botão do filtro de linha está ligado?", ("sim", "nao")),
        ("carregador_tem_indicador", "O carregador do notebook tem uma luz indicadora?", ("sim", "nao")),
        ("indicador_carregador_aceso", "A luz indicadora do carregador acende quando ele está na tomada?", ("sim", "nao")),
        ("carregador_conectado", "O carregador está conectado ao notebook?", ("sim", "nao")),
        ("liga_com_carregador", "O notebook liga quando o carregador está conectado?", ("sim", "nao")),
        ("liga_sem_carregador", "O notebook liga quando o carregador está desconectado?", ("sim", "nao")),
        ("tela_com_imagem", "A tela mostra alguma imagem depois que você aperta o botão de ligar?", ("sim", "nao")),
        ("monitor_ligado", "A luz indicadora do monitor está acesa?", ("sim", "nao")),
        ("cabo_video_no_monitor", "O cabo de vídeo está encaixado no monitor?", ("sim", "nao")),
        ("cabo_video_no_computador", "O cabo de vídeo está encaixado no computador?", ("sim", "nao")),
    ],
    "sistema_nao_inicia": [
        ("tipo_equipamento", "O equipamento é um notebook ou um computador de mesa?", ("notebook", "desktop")),
        ("mensagem_disco_nao_encontrado", "Aparece uma mensagem dizendo que o disco ou dispositivo de inicialização não foi encontrado?", ("sim", "nao")),
        ("cliques_no_disco", "Você ouve cliques ou estalos vindos do disco, diferentes do barulho da ventoinha?", ("sim", "nao")),
        ("reinicia_sem_parar", "O computador reinicia sozinho repetidas vezes antes da tela de login?", ("sim", "nao")),
        ("tela_cinza_persistente", "Depois de ligar, a tela fica cinza e não chega à tela de login?", ("sim", "nao")),
        ("tem_dispositivo_usb_conectado", "Há algum pendrive ou outro dispositivo USB conectado ao computador?", ("sim", "nao")),
        ("iniciou_apos_desconectar_usb", "Depois de desconectar os dispositivos USB, o computador chegou à tela de login?", ("sim", "nao")),
        ("problema_apos_atualizacao", "O problema começou logo depois de uma atualização do sistema?", ("sim", "nao")),
        ("reparo_automatico_disponivel", "A tela mostra uma opção chamada Reparo Automático ou Reparo de Inicialização?", ("sim", "nao")),
    ],
    "lento": [
        ("tipo_equipamento", "O equipamento é um notebook ou um computador de mesa?", ("notebook", "desktop")),
        ("esquenta_muito", "O computador fica muito quente durante o uso?", ("sim", "nao")),
        ("ruido_alto_ventoinha", "A ventoinha faz muito barulho ou funciona sem parar?", ("sim", "nao")),
        ("cliques_no_disco", "Você ouve cliques ou estalos vindos do disco, diferentes do barulho da ventoinha?", ("sim", "nao")),
        ("armazenamento_quase_cheio", "O computador avisa que o espaço de armazenamento está quase cheio?", ("sim", "nao")),
        ("melhora_ao_fechar_programas", "O computador fica mais rápido ao fechar programas que não está usando?", ("sim", "nao")),
        ("programas_fecham_sozinhos", "Programas fecham sozinhos ou mostram mensagens de erro durante o uso?", ("sim", "nao")),
    ],
    "nao_carrega": [
        ("tipo_equipamento", "O equipamento é um notebook ou um computador de mesa?", ("notebook", "desktop")),
        ("carregador_conectado", "O carregador está conectado ao notebook?", ("sim", "nao")),
        ("carregador_conectando_desconectando", "O carregador fica conectando e desconectando sozinho?", ("sim", "nao")),
        ("carregador_tem_indicador", "O carregador tem uma luz indicadora?", ("sim", "nao")),
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
    "desliga_sozinho": [
        ("tipo_equipamento", "O equipamento é um notebook ou um computador de mesa?", ("notebook", "desktop")),
        ("equipamento_muito_quente", "O equipamento fica muito quente antes de desligar?", ("sim", "nao")),
        ("ventoinha_barulhenta_ou_parada", "A ventoinha está muito barulhenta ou parada?", ("sim", "nao")),
        ("desliga_em_uso_pesado", "O equipamento desliga durante jogos, vídeos ou outros usos pesados?", ("sim", "nao")),
        ("sem_limpeza_ha_mais_de_1_ano", "O interior do equipamento não é limpo há mais de um ano?", ("sim", "nao")),
        ("usa_sobre_cama_ou_sofa", "O notebook é usado sobre cama ou sofá?", ("sim", "nao")),
        ("desliga_ao_mexer_no_cabo_ou_tomada", "O equipamento desliga ao mexer no cabo ou na tomada?", ("sim", "nao")),
        ("energia_da_casa_oscila", "A energia da casa oscila ou faltam luzes em outras ocasiões?", ("sim", "nao")),
        ("cheiro_de_queimado", "Há cheiro de queimado ou fumaça?", ("sim", "nao")),
        ("desliga_ao_tirar_carregador", "O notebook desliga quando o carregador é retirado?", ("sim", "nao")),
        ("tela_azul_antes_de_desligar", "Uma tela azul aparece antes do desligamento?", ("sim", "nao")),
        ("instalou_programa_ou_driver_recentemente", "Você instalou algum programa ou driver recentemente?", ("sim", "nao")),
    ],
}

SINTOMAS = {
    "1": ("nao_liga", "Computador não liga"),
    "2": ("sistema_nao_inicia", "Sistema não inicia"),
    "3": ("lento", "Computador lento, travando ou fechando programas"),
    "4": ("nao_carrega", "Notebook não carrega"),
    "5": ("internet_nao_conecta", "Internet não conecta"),
    "6": ("desliga_sozinho", "Computador desliga sozinho"),
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
    if fato == "chave_fonte_ligada":
        return respostas.get("tipo_equipamento") == "desktop"
    if fato == "usa_filtro_linha":
        return respostas.get("tipo_equipamento") == "desktop"
    if fato == "filtro_linha_ligado":
        return respostas.get("usa_filtro_linha") == "sim"
    if fato == "carregador_tem_indicador":
        return respostas.get("tipo_equipamento") == "notebook"
    if fato == "indicador_carregador_aceso":
        return respostas.get("carregador_tem_indicador") == "sim"
    if fato in {"carregador_conectado", "liga_com_carregador", "liga_sem_carregador"}:
        return respostas.get("tipo_equipamento") == "notebook"
    if fato in {"monitor_ligado", "cabo_video_no_monitor", "cabo_video_no_computador"}:
        return (
            respostas.get("tipo_equipamento") == "desktop"
            and respostas.get("tela_com_imagem") == "nao"
        )
    if fato == "tela_com_imagem":
        return respostas.get("sinal_de_vida") == "sim"
    if fato == "iniciou_apos_desconectar_usb":
        return respostas.get("tem_dispositivo_usb_conectado") == "sim"
    if fato == "reparo_automatico_disponivel":
        return respostas.get("problema_apos_atualizacao") == "sim"
    if fato == "funciona_com_cabo_rede":
        return respostas.get("cabo_rede_conectado") == "sim"
    if fato == "usa_sobre_cama_ou_sofa":
        return respostas.get("tipo_equipamento") == "notebook"
    if fato == "desliga_ao_tirar_carregador":
        return respostas.get("tipo_equipamento") == "notebook"
    if fato == "instalou_programa_ou_driver_recentemente":
        return respostas.get("tela_azul_antes_de_desligar") == "sim"
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
        explicacao = resultado.get(
            "por_que",
            resultado.get("explicacao", "Não há explicação registrada."),
        )
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
    try:
        sintoma = escolher_sintoma(input_fn)
        respostas = coletar_respostas(sintoma, input_fn)
    except (EOFError, KeyboardInterrupt):
        print("\n\nAtendimento encerrado antes de concluir. Nenhuma informação foi salva.")
        return
    resultados = inferir(sintoma, respostas)
    exibir_resultados(resultados)


def executar_questionario(
    input_fn: Callable[[str], str] = input,
) -> tuple[str, dict[str, str]]:
    """Executa somente a coleta do sintoma e das respostas do cliente."""
    sintoma = escolher_sintoma(input_fn)
    respostas = coletar_respostas(sintoma, input_fn)
    return sintoma, respostas


if __name__ == "__main__":
    from motor import inferir

    executar_interface(inferir)

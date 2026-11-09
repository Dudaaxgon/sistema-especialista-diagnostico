# Regras — Notebook não carrega

Sintoma: `nao_carrega`  
Responsável: Luiza Ribeiro

## Fatos de entrada (perguntas ao cliente)

| Fato | Pergunta | Respostas |
|---|---|---|
| `tipo_equipamento` | O equipamento é um notebook ou um computador de mesa? | notebook / desktop |
| `carregador_conectado` | O carregador está conectado ao notebook? | sim / nao |
| `carregador_conectando_desconectando` | O carregador fica conectando e desconectando sozinho? | sim / nao |
| `indicador_carregador_aceso` | A luz indicadora do carregador acende quando ele está na tomada? | sim / nao |
| `notebook_indica_carregamento` | O notebook mostra que está carregando quando o carregador é conectado? | sim / nao |
| `bateria_aumenta_carga` | A porcentagem da bateria aumenta depois de alguns minutos conectado? | sim / nao |
| `tomada_funciona` | Outro aparelho funciona na tomada usada pelo carregador? | sim / nao |
| `testou_outra_tomada` | Você testou o carregador em outra tomada? | sim / nao |
| `funcionou_outra_tomada` | O carregador funcionou na outra tomada? | sim / nao |
| `carregador_ou_cabo_danificado` | O carregador ou o cabo tem cortes, rachaduras, partes expostas ou pinos tortos? | sim / nao |

Pergunte sobre `testou_outra_tomada` somente se `tomada_funciona = nao`.
Pergunte `funcionou_outra_tomada` somente se `testou_outra_tomada = sim`.

## Regras

### Significado da sigla
`NC` identifica o sintoma **“notebook não carrega”**.

### NC-R1 — Carregador conectado e notebook não reconhece a carga
SE:     tipo_equipamento = notebook
        E carregador_conectado = sim
        E notebook_indica_carregamento = nao
ENTÃO:  causa = possivel_falha_no_carregador_ou_entrada
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: O notebook não reconhece o carregador conectado. A falha pode estar no carregador, no cabo ou na entrada de energia e precisa de avaliação.

### NC-R2 — Carregador conectando e desconectando
SE:     tipo_equipamento = notebook
        E carregador_conectando_desconectando = sim
ENTÃO:  causa = mau_contato_no_carregador
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: O carregador conecta e desconecta sozinho, o que pode indicar mau contato no cabo, no conector ou na entrada do notebook.

### NC-R3 — Carregador sem indicador luminoso
SE:     tipo_equipamento = notebook
        E carregador_conectado = sim
        E indicador_carregador_aceso = nao
        E notebook_indica_carregamento = nao
ENTÃO:  causa = possivel_carregador_defeituoso
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: A luz do carregador não acende e o notebook também não indica carregamento. O carregador pode estar com defeito; não tente abri-lo.

### NC-R4 — Bateria não aumenta a carga
SE:     tipo_equipamento = notebook
        E carregador_conectado = sim
        E notebook_indica_carregamento = sim
        E bateria_aumenta_carga = nao
ENTÃO:  causa = possivel_falha_bateria
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: O notebook reconhece o carregador, mas a porcentagem da bateria não aumenta. A bateria pode estar desgastada ou com defeito.

### NC-R5 — Tomada original com problema
SE:     tipo_equipamento = notebook
        E tomada_funciona = nao
        E testou_outra_tomada = sim
        E funcionou_outra_tomada = sim
ENTÃO:  causa = tomada_original_com_problema
TIPO:   final
AÇÃO:   cliente_resolve
EXPLICAÇÃO: O carregador funcionou em outra tomada. Use uma tomada que funcione e solicite avaliação elétrica para a tomada original, se necessário.

### NC-R6 — Cabo ou carregador danificado
SE:     tipo_equipamento = notebook
        E carregador_ou_cabo_danificado = sim
ENTÃO:  causa = carregador_ou_cabo_danificado
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: Um cabo cortado, rachado ou com partes expostas oferece risco e pode impedir o carregamento. Pare de usá-lo e procure a assistência.

# Regras — Computador não liga

Sintoma: `nao_liga`
Responsável: Maria Eduarda Pires Gonçalves Medrado - 1250101767

## Fatos de entrada (perguntas ao cliente)

| Fato | Pergunta | Respostas |
|---|---|---|
| `tipo_equipamento` | Qual é o seu equipamento? | notebook / desktop |
| `sinal_de_vida` | Ao apertar o botão, alguma luz acende ou algum ventilador gira? | sim / nao |
| `cabo_energia_conectado` | O cabo de energia está encaixado na entrada do computador? | sim / nao |
| `tomada_funciona` | Outro aparelho funciona na tomada usada pelo computador? | sim / nao |
| `testou_outra_tomada` | Você testou o computador em outra tomada? | sim / nao |
| `funcionou_outra_tomada` | O computador ligou nessa outra tomada? | sim / nao |
| `chave_fonte_ligada` | No desktop, a chave atrás do gabinete está na posição `I`? | sim / nao |
| `usa_filtro_linha` | O computador está ligado a um filtro de linha? | sim / nao |
| `filtro_linha_ligado` | Se usa filtro de linha, o botão dele está ligado? | sim / nao |
| `carregador_tem_indicador` | O carregador do notebook tem uma luz indicadora? | sim / nao |
| `indicador_carregador_aceso` | Se o carregador tem luz indicadora, ela acende quando ele está na tomada? | sim / nao |
| `carregador_conectado` | O carregador está conectado ao notebook? | sim / nao |
| `liga_com_carregador` | O notebook liga quando o carregador está conectado? | sim / nao |
| `liga_sem_carregador` | O notebook liga quando o carregador está desconectado? | sim / nao |
| `tela_com_imagem` | A tela mostra alguma imagem depois que você aperta o botão de ligar? | sim / nao |
| `monitor_ligado` | A luz indicadora do monitor está acesa? | sim / nao |
| `cabo_video_no_monitor` | O cabo de vídeo está encaixado no monitor? | sim / nao |
| `cabo_video_no_computador` | O cabo de vídeo está encaixado no computador? | sim / nao |

As perguntas sobre filtro de linha, carregador, tela e monitor só devem ser feitas quando forem aplicáveis. Pergunte `funcionou_outra_tomada` somente se `testou_outra_tomada = sim`; as duas respostas são fatos distintos. Pergunte sobre a luz indicadora do carregador somente se ele tiver indicador.

## Regras

### Significado da sigla
`NL` significa **“não liga”**. Assim, `NL-R1` identifica a primeira regra desse sintoma.

### NL-R1 — Problema na tomada original
SE:     testou_outra_tomada = sim
        E funcionou_outra_tomada = sim
ENTÃO:  causa = tomada_original_com_problema
TIPO:   final
AÇÃO:   cliente_resolve
EXPLICAÇÃO: O computador ligou em outra tomada. Use essa tomada e, se precisar verificar a tomada original, procure um eletricista.

### NL-R2 — Cabo de energia desconectado
SE:     cabo_energia_conectado = nao
        E sinal_de_vida = nao
ENTÃO:  causa = cabo_solto
TIPO:   final
AÇÃO:   cliente_resolve
EXPLICAÇÃO: O cabo não está encaixado na entrada de energia do computador. Com o equipamento desligado, encaixe-o corretamente.

### NL-R3 — Chave da fonte do desktop desligada
SE:     tipo_equipamento = desktop
        E chave_fonte_ligada = nao
        E sinal_de_vida = nao
ENTÃO:  causa = chave_fonte_desligada
TIPO:   final
AÇÃO:   cliente_resolve
EXPLICAÇÃO: A chave atrás do gabinete está na posição desligada (`O`). Coloque-a na posição ligada (`I`) e tente novamente.

### NL-R4 — Filtro de linha desligado
SE:     usa_filtro_linha = sim
        E filtro_linha_ligado = nao
        E sinal_de_vida = nao
ENTÃO:  causa = filtro_linha_desligado
TIPO:   final
AÇÃO:   cliente_resolve
EXPLICAÇÃO: O botão do filtro de linha está desligado. Ligue-o e tente iniciar o computador novamente.

### NL-R5 — Possível problema na bateria do notebook
SE:     tipo_equipamento = notebook
        E liga_com_carregador = sim
        E liga_sem_carregador = nao
ENTÃO:  causa = possivel_falha_bateria
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: O notebook liga conectado ao carregador, mas não liga sem ele. A bateria pode estar desgastada ou com defeito e precisa de avaliação.

### NL-R6 — Possível carregador defeituoso
SE:     tipo_equipamento = notebook
        E carregador_tem_indicador = sim
        E indicador_carregador_aceso = nao
        E liga_com_carregador = nao
ENTÃO:  causa = possivel_carregador_defeituoso
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: A luz do carregador não acende e o notebook não liga conectado a ele. O carregador pode estar com defeito; procure avaliação técnica ou teste com um carregador compatível conhecido, sem abrir o equipamento.

### NL-R7 — Alimentação externa verificada em desktop sem filtro de linha
SE:     tipo_equipamento = desktop
        E cabo_energia_conectado = sim
        E tomada_funciona = sim
        E chave_fonte_ligada = sim
        E usa_filtro_linha = nao
ENTÃO:  alimentacao_externa_ok
TIPO:   intermediária
EXPLICAÇÃO: O cabo está conectado, a tomada funciona, a chave da fonte está ligada e não há filtro de linha no caminho. As verificações externas básicas estão corretas.

### NL-R8 — Alimentação externa verificada em desktop com filtro de linha
SE:     tipo_equipamento = desktop
        E cabo_energia_conectado = sim
        E tomada_funciona = sim
        E chave_fonte_ligada = sim
        E usa_filtro_linha = sim
        E filtro_linha_ligado = sim
ENTÃO:  alimentacao_externa_ok
TIPO:   intermediária
EXPLICAÇÃO: O cabo está conectado, a tomada funciona, a chave da fonte e o filtro de linha estão ligados. As verificações externas básicas estão corretas.

### NL-R9 — Alimentação externa verificada em notebook
SE:     tipo_equipamento = notebook
        E cabo_energia_conectado = sim
        E tomada_funciona = sim
        E carregador_conectado = sim
        E carregador_tem_indicador = sim
        E indicador_carregador_aceso = sim
ENTÃO:  alimentacao_externa_ok
TIPO:   intermediária
EXPLICAÇÃO: A tomada funciona, o carregador está conectado e sua luz indicadora acende. As verificações externas básicas estão corretas.

### NL-R10 — Possível falha interna de alimentação
SE:     alimentacao_externa_ok
        E sinal_de_vida = nao
ENTÃO:  causa = possivel_falha_interna_energia
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: As verificações externas básicas estão corretas, mas o computador não dá sinal de vida. Pode haver uma falha interna de alimentação; é necessária avaliação técnica.

### NL-R11 — Computador ligado, mas sem imagem
SE:     sinal_de_vida = sim
        E tela_com_imagem = nao
ENTÃO:  computador_liga_sem_imagem
TIPO:   intermediária
EXPLICAÇÃO: O computador dá sinal de vida, mas a tela não mostra imagem. As regras seguintes verificam causas simples no desktop ou indicam avaliação técnica.

### NL-R12 — Sinal de vida, mas monitor desligado
SE:     tipo_equipamento = desktop
        E computador_liga_sem_imagem
        E monitor_ligado = nao
ENTÃO:  causa = monitor_desligado
TIPO:   final
AÇÃO:   cliente_resolve
EXPLICAÇÃO: O computador dá sinal de vida, mas a luz do monitor está apagada. Ligue o monitor e verifique se a imagem aparece.

### NL-R13 — Cabo de vídeo desconectado do monitor
SE:     tipo_equipamento = desktop
        E computador_liga_sem_imagem
        E cabo_video_no_monitor = nao
ENTÃO:  causa = cabo_video_desconectado
TIPO:   final
AÇÃO:   cliente_resolve
EXPLICAÇÃO: O computador dá sinal de vida, mas o cabo de vídeo não está encaixado no monitor. Com os aparelhos desligados, conecte o cabo ao monitor.

### NL-R14 — Cabo de vídeo desconectado do computador
SE:     tipo_equipamento = desktop
        E computador_liga_sem_imagem
        E cabo_video_no_computador = nao
ENTÃO:  causa = cabo_video_desconectado
TIPO:   final
AÇÃO:   cliente_resolve
EXPLICAÇÃO: O computador dá sinal de vida, mas o cabo de vídeo não está encaixado no computador. Com os aparelhos desligados, conecte o cabo ao computador.

### NL-R15 — Desktop sem imagem com monitor e cabos conectados
SE:     tipo_equipamento = desktop
        E computador_liga_sem_imagem
        E monitor_ligado = sim
        E cabo_video_no_monitor = sim
        E cabo_video_no_computador = sim
ENTÃO:  causa = possivel_falha_de_video
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: O computador dá sinal de vida, o monitor está ligado e os cabos estão conectados, mas não aparece imagem. Pode haver uma falha no monitor ou na saída de vídeo; é necessária avaliação técnica.

### NL-R16 — Notebook dá sinal de vida, mas a tela fica preta
SE:     tipo_equipamento = notebook
        E computador_liga_sem_imagem
ENTÃO:  causa = possivel_falha_na_tela_ou_video
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: O notebook dá sinal de vida, mas a tela não mostra imagem. Como não há um monitor ou cabo externo simples para verificar, procure avaliação técnica.

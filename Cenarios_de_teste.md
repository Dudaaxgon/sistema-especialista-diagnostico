# Cenários de teste do Dr. Byte

Os cenários abaixo simulam relatos de clientes. As respostas foram escolhidas
para exercitar regras diferentes da base; o diagnóstico é uma hipótese de
triagem, não uma confirmação técnica do defeito.

## 1. Computador não liga

### Cenário 1 — Tomada com problema

**Cliente:** “Meu computador não ligava na tomada de sempre. Testei em outra
tomada e funcionou.”

**Respostas:** `testou_outra_tomada = sim`;
`funcionou_outra_tomada = sim`.

**Diagnóstico esperado:** `tomada_original_com_problema` — orientar o cliente a
usar uma tomada que funcione e, se necessário, pedir a um eletricista que
verifique a tomada original. Regra `NL-R1`.

### Cenário 2 — Sem sinal de vida, mas energia externa verificada

**Cliente:** “É um computador de mesa. O cabo está encaixado, a tomada funciona,
a chave atrás do gabinete está ligada e não uso filtro de linha. Mesmo assim,
nenhuma luz acende e nenhuma ventoinha gira.”

**Respostas:** `tipo_equipamento = desktop`;
`cabo_energia_conectado = sim`; `tomada_funciona = sim`;
`chave_fonte_ligada = sim`; `usa_filtro_linha = nao`;
`sinal_de_vida = nao`.

**Diagnóstico esperado:** `possivel_falha_interna_energia` — encaminhar para
avaliação técnica. Regra intermediária `NL-R7` e regra final `NL-R10`.

## 2. Sistema não inicia

### Cenário 1 — Disco não encontrado

**Cliente:** “Quando ligo, aparece uma mensagem dizendo que o disco de
inicialização não foi encontrado.”

**Respostas:** `mensagem_disco_nao_encontrado = sim`.

**Diagnóstico esperado:** `possivel_falha_disco` — encaminhar para avaliação
técnica. Regras `SNI-R1` e `SNI-R3`.

### Cenário 2 — Reinicia sem sinais de problema no disco

**Cliente:** “O computador reinicia antes de chegar à tela de login. Não aparece
mensagem de disco e não ouço cliques ou estalos.”

**Respostas:** `reinicia_sem_parar = sim`;
`mensagem_disco_nao_encontrado = nao`; `cliques_no_disco = nao`.

**Diagnóstico esperado:** `possivel_falha_no_sistema` — encaminhar para
avaliação técnica. Regra `SNI-R5`, depois de as respostas relevantes permitirem
concluir que não há indícios informados de problema no disco.

## 3. Computador lento, travando ou fechando programas

### Cenário 1 — Pouco espaço disponível

**Cliente:** “O computador está lento e aparece um aviso de que o armazenamento
está quase cheio.”

**Respostas:** `armazenamento_quase_cheio = sim`.

**Diagnóstico esperado:** `pouco_espaco_armazenamento` — liberar espaço com
cuidado, sem apagar arquivos do sistema. Regra `LEN-R8`.

### Cenário 2 — Superaquecimento

**Cliente:** “Meu notebook fica muito quente e a ventoinha faz bastante barulho
enquanto ele está lento.”

**Respostas:** `tipo_equipamento = notebook`; `esquenta_muito = sim`;
`ruido_alto_ventoinha = sim`.

**Diagnóstico esperado:** `possivel_superaquecimento` — encaminhar para
avaliação da refrigeração. Regra intermediária `LEN-R1` e regra final `LEN-R3`.

## 4. Notebook não carrega

### Cenário 1 — Tomada original sem energia

**Cliente:** “Na tomada de sempre nem outro aparelho funciona. Testei o
carregador em outra tomada e o notebook começou a carregar.”

**Respostas:** `tipo_equipamento = notebook`; `tomada_funciona = nao`;
`testou_outra_tomada = sim`; `funcionou_outra_tomada = sim`.

**Diagnóstico esperado:** `tomada_original_com_problema` — usar uma tomada que
funcione e solicitar uma verificação elétrica da original, se necessário.
Regra `NC-R5`.

### Cenário 2 — Carregador conecta e desconecta

**Cliente:** “A carga começa e para sozinha; o carregador fica conectando e
desconectando.”

**Respostas:** `tipo_equipamento = notebook`;
`carregador_conectando_desconectando = sim`.

**Diagnóstico esperado:** `mau_contato_no_carregador` — interromper tentativas
se houver dano visível e procurar avaliação técnica. Regra `NC-R2`.

## 5. Internet não conecta

### Cenário 1 — Wi-Fi desligado

**Cliente:** “A rede está disponível, mas percebi que o Wi-Fi do computador está
desligado. O modo avião também está desligado.”

**Respostas:** `wifi_ligado = nao`; `modo_aviao_ligado = nao`.

**Diagnóstico esperado:** `wi_fi_desligado` — ativar o Wi-Fi e tentar conectar
novamente. Regra `INT-R1`.

### Cenário 2 — Outros aparelhos também estão sem internet

**Cliente:** “O nome da rede aparece, mas meu celular também não conecta.
Reiniciei o roteador, esperei alguns minutos e a internet não voltou.”

**Respostas:** `rede_aparece = sim`;
`outros_dispositivos_conectam = nao`; `reiniciou_roteador = sim`;
`internet_voltou_apos_reiniciar = nao`.

**Diagnóstico esperado:** `possivel_falha_no_roteador_ou_provedor` — entrar em
contato com o provedor. Regras `INT-R7` e `INT-R4`.

## 6. Computador desliga sozinho

### Cenário 1 — Notebook usado sobre superfície macia e superaquecendo

**Cliente:** “Meu notebook fica muito quente e costuma desligar. Eu uso ele
apoiado na cama.”

**Respostas:** `tipo_equipamento = notebook`;
`equipamento_muito_quente = sim`; `usa_sobre_cama_ou_sofa = sim`.

**Diagnósticos esperados:** `limpeza_ou_pasta_termica` — encaminhar para
avaliação técnica — e `ventilacao_bloqueada` — testar o uso sobre uma superfície
firme. O sistema apresenta primeiro a orientação de bancada, pois um dos
diagnósticos requer avaliação. Regras `DS1`, `DS4` e `DS5`.

### Cenário 2 — Desktop desliga sob uso pesado, sem sinais de calor

**Cliente:** “Meu computador de mesa desliga quando estou jogando. Ele não fica
quente, a ventoinha não está barulhenta e a limpeza interna foi feita há menos
de um ano.”

**Respostas:** `tipo_equipamento = desktop`;
`desliga_em_uso_pesado = sim`; `equipamento_muito_quente = nao`;
`ventoinha_barulhenta_ou_parada = nao`;
`sem_limpeza_ha_mais_de_1_ano = nao`.

**Diagnóstico esperado:** `fonte_insuficiente_ou_defeituosa` — encaminhar para
avaliação técnica. Regra `DS6`, após as respostas relevantes descartarem a
conclusão intermediária `superaquecimento`.

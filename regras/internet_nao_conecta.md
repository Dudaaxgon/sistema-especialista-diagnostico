# Regras — Internet não conecta

Sintoma: `internet_nao_conecta`  
Responsável: Luiza Ribeiro

## Fatos de entrada (perguntas ao cliente)

| Fato | Pergunta | Respostas |
|---|---|---|
| `tipo_equipamento` | O equipamento é um notebook ou um computador de mesa? | notebook / desktop |
| `rede_aparece` | O nome da sua rede aparece na lista de redes disponíveis? | sim / nao |
| `outros_dispositivos_conectam` | Outro celular ou computador consegue conectar nessa mesma rede? | sim / nao |
| `wifi_ligado` | O Wi-Fi está ligado no equipamento? | sim / nao |
| `modo_aviao_ligado` | O modo avião está ligado? | sim / nao |
| `cabo_rede_conectado` | O cabo de rede está conectado corretamente ao computador? | sim / nao |
| `funciona_com_cabo_rede` | A internet funciona quando o computador é conectado por cabo de rede? | sim / nao |
| `reiniciou_roteador` | Você já reiniciou o roteador e esperou alguns minutos? | sim / nao |
| `internet_voltou_apos_reiniciar` | A internet voltou depois de reiniciar o roteador? | sim / nao |

Pergunte sobre `cabo_rede_conectado` e `funciona_com_cabo_rede` quando o equipamento puder ser testado com cabo.
Pergunte `internet_voltou_apos_reiniciar` somente se `reiniciou_roteador = sim`.

## Regras

### Significado da sigla
`INT` identifica o sintoma **“internet não conecta”**.

### INT-R1 — Wi-Fi desligado
SE:     wifi_ligado = nao
        E modo_aviao_ligado = nao
ENTÃO:  causa = wi_fi_desligado
TIPO:   final
AÇÃO:   cliente_resolve
EXPLICAÇÃO: O Wi-Fi está desligado. Ative o Wi-Fi nas configurações do equipamento e tente conectar novamente.

### INT-R2 — Modo avião ligado
SE:     modo_aviao_ligado = sim
ENTÃO:  causa = modo_aviao_ligado
TIPO:   final
AÇÃO:   cliente_resolve
EXPLICAÇÃO: O modo avião pode desativar as conexões de rede. Desative-o e ligue o Wi-Fi novamente.

### INT-R3 — Rede sem fio não aparece
SE:     rede_aparece = nao
        E funciona_com_cabo_rede = nao
ENTÃO:  causa = possivel_falha_no_adaptador_wifi
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: A rede não aparece, mas outros dispositvos conectam.

### INT-R4 — Problema no roteador ou na internet da residência
SE:     rede_compartilhada_indisponivel
        E reiniciou_roteador = sim
        E internet_voltou_apos_reiniciar = nao
ENTÃO:  causa = possivel_falha_no_roteador_ou_provedor
TIPO:   final
AÇÃO:   contacta_provedor
EXPLICAÇÃO: Outros dispositivos também não conectam e reiniciar o roteador não resolveu. O problema pode estar no roteador ou no provedor de internet.

### INT-R5 — Falha apenas no computador
SE:     rede_aparece = sim
        E outros_dispositivos_conectam = sim
        E wifi_ligado = sim
ENTÃO:  causa = possivel_configuracao_de_rede
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: A rede funciona para outros dispositivos, mas não conecta neste computador. Pode haver uma configuração ou falha no adaptador de rede.

### INT-R6 — Conexão funciona pelo cabo
SE:     cabo_rede_conectado = sim
        E funciona_com_cabo_rede = sim
ENTÃO:  causa = possivel_falha_no_wifi
TIPO:   final
AÇÃO:   cliente_resolve
EXPLICAÇÃO: A internet funciona pelo cabo de rede. O problema está provavelmente na conexão sem fio; use o cabo temporariamente e atualize ou verifique o adaptador Wi-Fi.

### INT-R7 — Outros dispositivos também estão sem conexão
SE:     rede_aparece = sim
        E outros_dispositivos_conectam = nao
ENTÃO:  rede_compartilhada_indisponivel
TIPO:   intermediária
EXPLICAÇÃO: A rede aparece no computador, mas outros dispositivos também não conseguem conectar. Isso indica que a indisponibilidade pode estar na rede compartilhada, no roteador ou no provedor.

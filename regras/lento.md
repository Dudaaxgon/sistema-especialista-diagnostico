# Regras — Computador lento, travando ou fechando programas

Sintoma: `lento`
Responsável: Maria Eduarda Pires Gonçalves Medrado - 1250101767

## Fatos de entrada (perguntas ao cliente)

| Fato | Pergunta | Respostas |
|---|---|---|
| `tipo_equipamento` | O equipamento é um notebook ou um computador de mesa? | notebook / desktop |
| `esquenta_muito` | O computador fica muito quente durante o uso? | sim / nao |
| `ruido_alto_ventoinha` | A ventoinha faz muito barulho, como se estivesse trabalhando sem parar? | sim / nao |
| `cliques_no_disco` | Você ouve cliques ou estalos repetidos, diferentes do barulho da ventoinha? | sim / nao |
| `armazenamento_quase_cheio` | O computador avisa que o espaço de armazenamento está quase cheio? | sim / nao |
| `melhora_ao_fechar_programas` | O computador fica mais rápido quando você fecha programas que não está usando? | sim / nao |
| `programas_fecham_sozinhos` | Programas fecham sozinhos ou mostram mensagens de erro durante o uso? | sim / nao |

## Regras

### Significado da sigla
`LEN` identifica o sintoma **“lento, travando ou fechando programas”**. Assim, `LEN-R1` identifica a primeira regra desse sintoma.

### LEN-R1 — Evidências de superaquecimento em notebook
SE:     tipo_equipamento = notebook
        E esquenta_muito = sim
        E ruido_alto_ventoinha = sim
ENTÃO:  superaquecimento
TIPO:   intermediária
EXPLICAÇÃO: Em um notebook, o aquecimento excessivo junto com a ventoinha trabalhando muito é compatível com superaquecimento.

### LEN-R2 — Evidências de superaquecimento em desktop
SE:     tipo_equipamento = desktop
        E esquenta_muito = sim
        E ruido_alto_ventoinha = sim
ENTÃO:  superaquecimento
TIPO:   intermediária
EXPLICAÇÃO: Em um computador de mesa, o aquecimento excessivo junto com a ventoinha trabalhando muito é compatível com superaquecimento.

### LEN-R3 — Possível lentidão causada por superaquecimento
SE:     superaquecimento
ENTÃO:  causa = possivel_superaquecimento
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: O superaquecimento pode reduzir o desempenho e causar travamentos. A refrigeração precisa ser avaliada; não abra o equipamento para tentar limpá-lo.

### LEN-R4 — Equipamento quente com ventoinha silenciosa
SE:     tipo_equipamento = notebook
        E esquenta_muito = sim
        E ruido_alto_ventoinha = nao
ENTÃO:  causa = possivel_falha_ventoinha
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: O notebook está muito quente, mas a ventoinha não faz barulho. A ventoinha pode não estar funcionando corretamente; desligue o equipamento e procure avaliação técnica.

### LEN-R5 — Desktop quente com ventoinha silenciosa
SE:     tipo_equipamento = desktop
        E esquenta_muito = sim
        E ruido_alto_ventoinha = nao
ENTÃO:  causa = possivel_falha_ventoinha
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: O computador de mesa está muito quente, mas a ventoinha não faz barulho. A ventoinha pode não estar funcionando corretamente; desligue o equipamento e procure avaliação técnica.

### LEN-R6 — Ruídos indicam possível problema no disco
SE:     cliques_no_disco = sim
ENTÃO:  problema_disco
TIPO:   intermediária
EXPLICAÇÃO: Cliques repetidos vindos da região do disco podem indicar falha. Evite insistir no uso e faça avaliação técnica, especialmente se houver arquivos importantes.

### LEN-R7 — Possível problema no disco
SE:     problema_disco
ENTÃO:  causa = possivel_falha_disco
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: Os cliques podem indicar uma falha no disco, mas só uma avaliação técnica pode confirmar a causa.

### LEN-R8 — Pouco espaço de armazenamento
SE:     armazenamento_quase_cheio = sim
ENTÃO:  causa = pouco_espaco_armazenamento
TIPO:   final
AÇÃO:   cliente_resolve
EXPLICAÇÃO: O pouco espaço disponível pode deixar o computador lento. Apague arquivos que não precisa ou mova-os para outro local, sem excluir arquivos do sistema.

### LEN-R9 — Muitos programas em uso
SE:     melhora_ao_fechar_programas = sim
ENTÃO:  causa = muitos_programas_em_uso
TIPO:   final
AÇÃO:   cliente_resolve
EXPLICAÇÃO: Se o computador melhora quando programas são fechados, a quantidade de programas abertos pode estar consumindo os recursos disponíveis. Deixe abertos apenas os que estiver usando.

### LEN-R10 — Programas fechando inesperadamente
SE:     programas_fecham_sozinhos = sim
ENTÃO:  causa = possivel_falha_de_memoria_ou_software
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: Programas fechando sozinhos podem estar relacionados à memória ou ao software. Como há mais de uma causa possível, é necessária avaliação para confirmar.
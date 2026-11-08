# Regras — Sistema não inicia

Sintoma: `sistema_nao_inicia`
Responsável: Maria Eduarda Pires Gonçalves Medrado - 1250101767

## Fatos de entrada (perguntas ao cliente)

| Fato | Pergunta | Respostas |
|---|---|---|
| `tipo_equipamento` | O equipamento é um notebook ou um computador de mesa? | notebook / desktop |
| `mensagem_disco_nao_encontrado` | Aparece alguma mensagem dizendo que o disco ou dispositivo de inicialização não foi encontrado? | sim / nao |
| `cliques_no_disco` | Você ouve cliques ou estalos repetidos, diferentes do barulho da ventoinha? | sim / nao |
| `reinicia_sem_parar` | O computador reinicia sozinho repetidas vezes antes de chegar à tela de login? | sim / nao |
| `tela_cinza_persistente` | Depois de ligar, a tela fica cinza e não chega à tela de login? | sim / nao |
| `tem_dispositivo_usb_conectado` | Há algum pendrive ou outro dispositivo USB conectado ao computador? | sim / nao |
| `iniciou_apos_desconectar_usb` | Depois de desconectar os dispositivos USB, o computador chegou à tela de login? | sim / nao |
| `problema_apos_atualizacao` | O problema começou logo depois de uma atualização do sistema? | sim / nao |
| `reparo_automatico_disponivel` | Aparece na tela uma opção chamada “Reparo Automático” ou “Reparo de Inicialização”? | sim / nao |

Pergunte `iniciou_apos_desconectar_usb` somente se `tem_dispositivo_usb_conectado = sim`. Pergunte sobre o reparo automático somente se o problema começou após uma atualização.

## Regras

### Significado da sigla
`SNI` significa **“sistema não inicia”**. Assim, `SNI-R1` identifica a primeira regra desse sintoma.

### SNI-R1 — Mensagem indica possível problema no disco
SE:     mensagem_disco_nao_encontrado = sim
ENTÃO:  problema_disco
TIPO:   intermediária
EXPLICAÇÃO: A mensagem informa que o computador não encontrou o disco ou dispositivo necessário para iniciar.

### SNI-R2 — Ruídos indicam possível problema no disco
SE:     cliques_no_disco = sim
ENTÃO:  problema_disco
TIPO:   intermediária
EXPLICAÇÃO: Cliques repetidos vindos da região do disco podem indicar falha. Evite insistir em ligar o computador para não agravar uma possível perda de dados.

### SNI-R3 — Possível falha no disco
SE:     problema_disco
ENTÃO:  causa = possivel_falha_disco
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: Há uma mensagem ou um ruído compatível com problema no disco. A causa precisa ser confirmada por avaliação técnica; se houver arquivos importantes, informe isso à assistência.

### SNI-R4 — Dispositivo externo impede a inicialização
SE:     tem_dispositivo_usb_conectado = sim
        E iniciou_apos_desconectar_usb = sim
ENTÃO:  causa = dispositivo_externo_impede_inicio
TIPO:   final
AÇÃO:   cliente_resolve
EXPLICAÇÃO: O computador chegou à tela de login depois que os dispositivos USB foram desconectados. Deixe-os desconectados e conecte um de cada vez apenas se precisar identificar qual causou o problema.

### SNI-R5 — Reinicialização repetida sem indício de disco
SE:     reinicia_sem_parar = sim
        E NÃO problema_disco
ENTÃO:  causa = possivel_falha_no_sistema
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: O computador reinicia antes de chegar à tela de login e não há sinais informados de problema no disco. Pode haver uma falha no sistema ou em outro componente; é necessária avaliação.

### SNI-R6 — Tela cinza persistente sem indício de disco
SE:     tela_cinza_persistente = sim
        E NÃO problema_disco
ENTÃO:  causa = possivel_falha_na_inicializacao
TIPO:   final
AÇÃO:   encaminhar_bancada
EXPLICAÇÃO: A tela permanece cinza e não há sinais informados de problema no disco. A causa pode estar no sistema ou em outro componente e precisa ser investigada.

### SNI-R7 — Reparo automático após atualização
SE:     problema_apos_atualizacao = sim
        E reparo_automatico_disponivel = sim
ENTÃO:  causa = possivel_falha_apos_atualizacao
TIPO:   final
AÇÃO:   cliente_resolve
EXPLICAÇÃO: Como o problema começou depois de uma atualização, tente a opção “Reparo Automático” ou “Reparo de Inicialização” oferecida pelo próprio sistema. Se não resolver, interrompa as tentativas e procure avaliação técnica; não escolha opções de redefinição ou formatação.

## Requisito para o motor de inferência

As condições `NÃO problema_disco` exigem suporte a negação no motor. O motor só deve considerar `problema_disco` falso depois de coletar todas as respostas aplicáveis e concluir a aplicação das regras que podem gerar essa conclusão. Se alguma resposta relevante estiver faltando, o estado é desconhecido — não falso — e SNI-R5/SNI-R6 não devem disparar.
# Dr. Byte — Sistema Especialista de Diagnóstico de Falhas da ByteFix

Protótipo de Sistema Especialista desenvolvido para a disciplina **Programação de Sistemas Especialistas** (Ciência da Computação — Universidade Veiga de Almeida).

---

## 1. Contexto de negócio

- **Empresa simulada:** ByteFix Assistência Técnica, uma assistência técnica de notebooks e computadores.
- **Problema de negócio:** muitos clientes levam o equipamento até a loja por problemas simples que poderiam resolver sozinhos (ex.: tomada com defeito), enquanto outros chegam sem nenhuma informação sobre o defeito. Isso gera visitas desnecessárias, filas e atendimento lento.
- **Solução:** o **Dr. Byte**, um sistema especialista de **pré-triagem online**, usado pelo próprio **cliente** antes de levar o equipamento. O sistema faz perguntas em linguagem simples, infere a causa provável do problema e indica a ação adequada, explicando o raciocínio utilizado.
- **Usuário:** cliente leigo (sem conhecimento técnico).

## 2. Escopo

### Tipos de equipamento
O primeiro fato informado pelo cliente é o **tipo de equipamento** (`notebook` ou `desktop`). Ele é usado como condição apenas nas regras em que o raciocínio muda entre os dois tipos; as demais regras valem para ambos.

### Sintomas cobertos
| Sintoma | Vale para | Responsável pelas regras |
|---|---|---|
| Não liga | Notebook e desktop (regras diferentes) | Maria Eduarda |
| Sistema não inicia (tela cinza ou reiniciando sem parar) | Notebook e desktop | Maria Eduarda |
| Lento, travando ou fechando programas | Notebook e desktop | Maria Eduarda |
| Não carrega (inclui carregador conectando e desconectando) | Somente notebook | Luiza |
| Internet não conecta (rede nem aparece) | Notebook e desktop | Luiza |
| Desliga sozinho após um tempo de uso | Notebook e desktop | Luciana |

### Evidências (pistas usadas por várias regras)
Algumas informações não são sintomas, mas pistas que ajudam a estreitar a causa. Exemplos:
- Ruído alto na ventoinha → evidência de superaquecimento
- Cliques ou estalos vindos do disco → evidência de problema no disco
- Programas fechando sozinhos → evidência de problema de memória

### Conclusões finais possíveis (ações da assistência)
- **Cliente resolve sozinho** (com instrução)
- **Encaminhar para bancada** (avaliação técnica)
- **Orçamento de troca de peça**
- **Acionar garantia / conserto não compensa**
- **Não foi possível concluir** com as informações fornecidas

## 3. Abordagem técnica

- **Linguagem:** Python
- **Justificativa:** Python foi escolhido por ser a linguagem trabalhada pela equipe e permitir representar fatos e regras com estruturas simples. Isso facilita implementar e explicar o motor de inferência e o módulo de explicação, além de integrar a interface de terminal.
- **Tipo de encadeamento:** encadeamento para frente. O motor parte das respostas coletadas, aplica as regras compatíveis com esses fatos e propaga conclusões intermediárias até não haver novas derivações, chegando a zero ou mais diagnósticos finais. Esse fluxo combina com a triagem, que começa pelas respostas do cliente e não por uma causa previamente escolhida. Condições negadas (`NÃO X`) só são avaliadas quando as entradas relevantes para provar `X` foram coletadas e as regras produtoras já foram consideradas, distinguindo fato falso de fato desconhecido.

## 4. Arquitetura

| Componente | Função | Arquivo |
|---|---|---|
| Base de conhecimento | Regras lidas dos arquivos Markdown da pasta `regras/` | `regras/*.md` |
| Memória de trabalho | Respostas coletadas na sessão atual (fatos conhecidos/desconhecidos) | Dicionário recebido por `motor.inferir` |
| Motor de inferência | Encadeamento para frente, propagação de conclusões intermediárias e tratamento de negação com fato desconhecido | `motor.py` |
| Módulo de explicação | Retorna causa, ação, regra(s) disparada(s) e justificativa ("por quê / como") | `motor.py` (campos `explicacao`, `como` e `por_que`) |
| Interface | Perguntas e respostas com o cliente (terminal) | `interface.py` |
| Testes automatizados | Validação do motor, explicação e cenários de inferência | `test_motor.py` |

## 5. Base de conhecimento

### Formato das regras
Cada regra deve seguir o modelo:

```
ID:        R1
SINTOMA:   nao_liga
SE:        trocou_tomada = sim
           E funcionou_outra_tomada = sim
ENTÃO:     causa = tomada_defeituosa
TIPO:      final            (intermediária ou final)
AÇÃO:      cliente_resolve
EXPLICAÇÃO: O equipamento funcionou em outra tomada, então o defeito está na tomada original.
```

### Quando mais de uma regra é ativada
O motor deve verificar todas as regras do sintoma, sem parar na primeira que corresponder. Se mais de uma regra produzir um diagnóstico final, o Dr. Byte deve apresentar todos os diagnósticos distintos e suas explicações, sem escolher um deles arbitrariamente. Se as ações forem diferentes e pelo menos uma exigir `encaminhar_bancada`, essa orientação deve vir primeiro; ações de `cliente_resolve` não devem ser apresentadas como solução suficiente para os demais diagnósticos. Conclusões intermediárias servem para ativar outras regras e não são exibidas como diagnósticos finais.

### Glossário de conclusões intermediárias compartilhadas
Conclusões usadas por regras de mais de um sintoma. **Todas devem usar exatamente estes nomes.** Para criar uma nova, adicione aqui antes de usar.

| Nome | Significado | Usada nos sintomas |
|---|---|---|
| `superaquecimento` | O equipamento está esquentando além do normal | Desliga sozinho, Lento |
| `problema_disco` | Há indícios de falha no disco (HD/SSD) | Sistema não inicia, Lento |
| `alimentacao_externa_ok` | As verificações externas de energia (tomada, cabos e controles acessíveis) estão corretas | Não liga, Não carrega |

### Sintoma: desliga_sozinho

```
ID:        DS1
SINTOMA:   desliga_sozinho
SE:        equipamento_muito_quente = sim
ENTÃO:     superaquecimento = sim
TIPO:      intermediária
AÇÃO:      nenhuma
EXPLICAÇÃO: O equipamento está muito quente, o que indica superaquecimento.
```

```
ID:        DS2
SINTOMA:   desliga_sozinho
SE:        ventoinha_barulhenta_ou_parada = sim
ENTÃO:     superaquecimento = sim
TIPO:      intermediária
AÇÃO:      nenhuma
EXPLICAÇÃO: Ventoinha com barulho forte ou parada não resfria o equipamento, o que causa superaquecimento.
```

```
ID:        DS3
SINTOMA:   desliga_sozinho
SE:        desliga_em_uso_pesado = sim
           E sem_limpeza_ha_mais_de_1_ano = sim
ENTÃO:     superaquecimento = sim
TIPO:      intermediária
AÇÃO:      nenhuma
EXPLICAÇÃO: Desligar sob uso pesado em um equipamento sem limpeza há mais de 1 ano indica acúmulo de poeira e superaquecimento.
```

```
ID:        DS4
SINTOMA:   desliga_sozinho
SE:        superaquecimento = sim
           E tipo_equipamento = notebook
           E usa_sobre_cama_ou_sofa = sim
ENTÃO:     causa = ventilacao_bloqueada
TIPO:      final
AÇÃO:      cliente_resolve
EXPLICAÇÃO: O notebook superaquece e é usado sobre superfícies macias, que bloqueiam a saída de ar. Use-o sobre superfície firme.
```

```
ID:        DS5
SINTOMA:   desliga_sozinho
SE:        superaquecimento = sim
ENTÃO:     causa = limpeza_ou_pasta_termica
TIPO:      final
AÇÃO:      encaminhar_bancada
EXPLICAÇÃO: Há superaquecimento, e o motivo mais comum é poeira interna ou pasta térmica ressecada, que exigem limpeza técnica.
```

```
ID:        DS6
SINTOMA:   desliga_sozinho
SE:        tipo_equipamento = desktop
           E desliga_em_uso_pesado = sim
           E NÃO superaquecimento
ENTÃO:     causa = fonte_insuficiente_ou_defeituosa
TIPO:      final
AÇÃO:      encaminhar_bancada
EXPLICAÇÃO: Desliga sob uso pesado, mas sem sinais de calor, o que aponta para a fonte não entregar energia suficiente.
```

```
ID:        DS7
SINTOMA:   desliga_sozinho
SE:        desliga_ao_mexer_no_cabo_ou_tomada = sim
ENTÃO:     causa = mau_contato_energia
TIPO:      final
AÇÃO:      cliente_resolve
EXPLICAÇÃO: Desligar ao mexer no cabo ou na tomada indica mau contato. Troque o cabo ou a tomada.
```

```
ID:        DS8
SINTOMA:   desliga_sozinho
SE:        energia_da_casa_oscila = sim
           E NÃO superaquecimento
ENTÃO:     causa = problema_rede_eletrica
TIPO:      final
AÇÃO:      cliente_resolve
EXPLICAÇÃO: A energia da casa oscila e não há sinais de calor, então a rede elétrica é a causa provável. Use estabilizador ou nobreak.
```

```
ID:        DS9
SINTOMA:   desliga_sozinho
SE:        cheiro_de_queimado = sim
ENTÃO:     causa = fonte_com_defeito
TIPO:      final
AÇÃO:      encaminhar_bancada
EXPLICAÇÃO: Cheiro de queimado indica falha elétrica. Desligue da tomada e não use até a avaliação técnica.
```

```
ID:        DS10
SINTOMA:   desliga_sozinho
SE:        tipo_equipamento = notebook
           E desliga_ao_tirar_carregador = sim
ENTÃO:     causa = bateria_com_defeito
TIPO:      final
AÇÃO:      encaminhar_bancada
EXPLICAÇÃO: O notebook desliga assim que o carregador é removido, o que mostra que a bateria não segura carga.
```

```
ID:        DS11
SINTOMA:   desliga_sozinho
SE:        tela_azul_antes_de_desligar = sim
           E instalou_programa_ou_driver_recentemente = sim
ENTÃO:     causa = problema_software
TIPO:      final
AÇÃO:      cliente_resolve
EXPLICAÇÃO: A tela azul começou depois de instalar um programa ou driver, então o software novo é a causa provável. Desinstale-o.
```

```
ID:        DS12
SINTOMA:   desliga_sozinho
SE:        tela_azul_antes_de_desligar = sim
           E instalou_programa_ou_driver_recentemente = nao
           E NÃO superaquecimento
ENTÃO:     causa = problema_memoria_ram
TIPO:      final
AÇÃO:      encaminhar_bancada
EXPLICAÇÃO: Tela azul sem mudança de software e sem superaquecimento aponta para defeito na memória RAM.
```

### Dicionário de regras

A base completa de regras está em `regras/*.md` (59 regras no total), que é o formato lido pelo motor. Abaixo, um resumo das regras por sintoma; consulte os arquivos de regras para condições, explicações e perguntas detalhadas.

| ID | Sintoma | Condições (SE) — resumo | Conclusão (ENTÃO) | Tipo |
|---|---|---|---|---|
| NL-R1 | nao_liga | testou outra tomada e funcionou | tomada_original_com_problema → cliente_resolve | final |
| NL-R2 | nao_liga | cabo de energia desconectado e sem sinal de vida | cabo_solto → cliente_resolve | final |
| NL-R3 | nao_liga | desktop, chave da fonte desligada, sem sinal de vida | chave_fonte_desligada → cliente_resolve | final |
| NL-R4 | nao_liga | filtro de linha desligado, sem sinal de vida | filtro_linha_desligado → cliente_resolve | final |
| NL-R5 | nao_liga | notebook liga com carregador, mas não sem ele | possivel_falha_bateria → encaminhar_bancada | final |
| NL-R6 | nao_liga | notebook, indicador do carregador apagado e não liga com ele | possivel_carregador_defeituoso → encaminhar_bancada | final |
| NL-R7..R9 | nao_liga | verificações externas de energia corretas (desktop/notebook) | alimentacao_externa_ok | intermediária |
| NL-R10 | nao_liga | alimentacao_externa_ok e sem sinal de vida | possivel_falha_interna_energia → encaminhar_bancada | final |
| NL-R11 | nao_liga | sinal de vida, mas sem imagem na tela | computador_liga_sem_imagem | intermediária |
| NL-R12..R14 | nao_liga | desktop sem imagem por monitor desligado/cabo solto | monitor_desligado / cabo_video_desconectado → cliente_resolve | final |
| NL-R15 | nao_liga | desktop sem imagem com monitor e cabos ok | possivel_falha_de_video → encaminhar_bancada | final |
| NL-R16 | nao_liga | notebook com sinal de vida e tela preta | possivel_falha_na_tela_ou_video → encaminhar_bancada | final |
| SNI-R1 | sistema_nao_inicia | mensagem de disco/dispositivo não encontrado | problema_disco | intermediária |
| SNI-R2 | sistema_nao_inicia | cliques/estalos na região do disco | problema_disco | intermediária |
| SNI-R3 | sistema_nao_inicia | problema_disco | possivel_falha_disco → encaminhar_bancada | final |
| SNI-R4 | sistema_nao_inicia | iniciou após desconectar USB | dispositivo_externo_impede_inicio → cliente_resolve | final |
| SNI-R5 | sistema_nao_inicia | reinicia sem parar e NÃO problema_disco | possivel_falha_no_sistema → encaminhar_bancada | final |
| SNI-R6 | sistema_nao_inicia | tela cinza persistente e NÃO problema_disco | possivel_falha_na_inicializacao → encaminhar_bancada | final |
| SNI-R7 | sistema_nao_inicia | problema após atualização com reparo automático disponível | possivel_falha_apos_atualizacao → cliente_resolve | final |
| LEN-R1..R2 | lento | equipamento esquenta muito e ventoinha com ruído alto | superaquecimento | intermediária |
| LEN-R3 | lento | superaquecimento | possivel_superaquecimento → encaminhar_bancada | final |
| LEN-R4..R5 | lento | muito quente, mas ventoinha silenciosa | possivel_falha_ventoinha → encaminhar_bancada | final |
| LEN-R6 | lento | cliques/estalos no disco | problema_disco | intermediária |
| LEN-R7 | lento | problema_disco | possivel_falha_disco → encaminhar_bancada | final |
| LEN-R8 | lento | armazenamento quase cheio | pouco_espaco_armazenamento → cliente_resolve | final |
| LEN-R9 | lento | melhora ao fechar programas | muitos_programas_em_uso → cliente_resolve | final |
| LEN-R10 | lento | programas fecham sozinhos | possivel_falha_de_memoria_ou_software → encaminhar_bancada | final |
| DS1..DS3 | desliga_sozinho | sinais de calor, ventoinha ou uso pesado sem limpeza | superaquecimento | intermediária |
| DS4 | desliga_sozinho | superaquecimento, notebook usado em superfície macia | ventilacao_bloqueada → cliente_resolve | final |
| DS5 | desliga_sozinho | superaquecimento | limpeza_ou_pasta_termica → encaminhar_bancada | final |
| DS6 | desliga_sozinho | desktop desliga em uso pesado e NÃO superaquecimento | fonte_insuficiente_ou_defeituosa → encaminhar_bancada | final |
| DS7 | desliga_sozinho | desliga ao mexer no cabo/tomada | mau_contato_energia → cliente_resolve | final |
| DS8 | desliga_sozinho | energia oscila e NÃO superaquecimento | problema_rede_eletrica → cliente_resolve | final |
| DS9 | desliga_sozinho | cheiro de queimado | fonte_com_defeito → encaminhar_bancada | final |
| DS10 | desliga_sozinho | notebook desliga ao tirar carregador | bateria_com_defeito → encaminhar_bancada | final |
| DS11 | desliga_sozinho | tela azul após instalar programa/driver | problema_software → cliente_resolve | final |
| DS12 | desliga_sozinho | tela azul sem mudança recente e NÃO superaquecimento | problema_memoria_ram → encaminhar_bancada | final |
| NC-R1..R7 | nao_carrega | regras de carregamento, tomada e bateria (notebook) | ver `regras/nao_carrega.md` | intermediária/final |
| INT-R1..R7 | internet_nao_conecta | regras de Wi-Fi, cabo, roteador e rede | ver `regras/internet_nao_conecta.md` | intermediária/final |

## 6. Extensões futuras

Sintomas planejados para demonstrar a extensibilidade da base de conhecimento (adicionados apenas editando o arquivo de regras, sem alterar o código):
- Congelamento total do sistema
- Programas fechando sozinhos (como sintoma próprio)

## 7. Como executar

Requisitos: Python 3 (testado com Python 3.14 no ambiente atual). Não há dependências externas obrigatórias.

```bash
# Interface de terminal (questionários atualmente cadastrados: "não carrega" e "internet não conecta")
python3 interface.py

# Alternativa equivalente (a interface usa o motor de inferência)
python3 motor.py
```

O comando inicia a interface de terminal, apresenta os sintomas disponíveis no menu, coleta as respostas aplicáveis e exibe o(s) diagnóstico(s) gerado(s) pelo motor de inferência (com explicação).

O motor carrega automaticamente as regras de `regras/*.md`. Também é possível usar o motor diretamente em Python para inferir sobre qualquer sintoma cuja base de regras já exista:

```python
from motor import inferir

resultados = inferir("nao_liga", {"testou_outra_tomada": "sim", "funcionou_outra_tomada": "sim"})
print(resultados)
```

## 8. Testes

Os testes automatizados do motor ficam em `test_motor.py` e validam encadeamento para frente, propagação de conclusões intermediárias, explicação ("como/por quê"), tratamento de negação com fatos desconhecidos e cenários representativos dos sintomas.

```bash
python3 -m unittest -v test_motor.py
```

> Observação: os cenários devem ser ampliados conforme os cenários de teste em texto definidos pela equipe (Luciana), mantendo os testes alinhados ao comportamento esperado das regras.

## 9. Integrantes

| Nome completo | Responsabilidade |
|---|---|
| Maria Eduarda Pires | Motor de inferência, módulo de explicação, testes automatizados, regras "não liga", "sistema não inicia" e "lento", integração |
| Luiza Ribeiro | Regras "não carrega" e "internet não conecta", interface e validação de entradas |
| Luciana Tavares | Regras "desliga sozinho", contexto de negócio, cenários de teste, dicionário de regras, roteiro do vídeo e PDF de entrega |

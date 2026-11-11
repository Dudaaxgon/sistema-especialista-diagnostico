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
- **Justificativa:** [escrever 2–3 frases — ex.: domínio da equipe, controle total sobre o motor de inferência e o módulo de explicação, facilidade para base de conhecimento externa (JSON) e testes automatizados, baixo risco de execução]
- **Tipo de encadeamento:** [a definir — para frente ou para trás, com justificativa]

## 4. Arquitetura

| Componente | Função | Arquivo |
|---|---|---|
| Base de conhecimento | Fatos e regras do domínio | [a definir] |
| Memória de trabalho | Fatos coletados na sessão atual | [a definir] |
| Motor de inferência | Aplica as regras sobre os fatos | [a definir] |
| Módulo de explicação | Justifica a conclusão ("por quê / como") | [a definir] |
| Interface | Perguntas e respostas com o cliente | [a definir] |

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
| ID | Sintoma | Condições (SE) | Conclusão (ENTÃO) | Tipo |
|---|---|---|---|---|
| R1 | nao_liga | trocou_tomada = sim E funcionou_outra_tomada = sim | tomada_defeituosa → cliente_resolve | final |
| R2 | | | | |
| DS1| desliga_sozinho | equipamento_muito_quente = sim | superaquecimento | intermediária |
| DS2| desliga_sozinho | ventoinha_barulhenta_ou_parada = sim | superaquecimento | intermediária |
| DS3| desliga_sozinho | desliga_em_uso_pesado = sim E sem_limpeza_ha_mais_de_1_ano = sim | superaquecimento | intermediária |
| DS4| desliga_sozinho | superaquecimento = sim E tipo_equipamento = notebook E usa_sobre_cama_ou_sofa = sim | ventilacao_bloqueada → cliente_resolve | final |
| DS5 | desliga_sozinho | superaquecimento = sim | limpeza_ou_pasta_termica → encaminhar_bancada | final |
| DS6 | desliga_sozinho | tipo_equipamento = desktop E desliga_em_uso_pesado = sim E NÃO superaquecimento | fonte_insuficiente_ou_defeituosa → encaminhar_bancada | final |
| DS7 | desliga_sozinho | desliga_ao_mexer_no_cabo_ou_tomada = sim | mau_contato_energia → cliente_resolve | final |
| DS8 | desliga_sozinho | energia_da_casa_oscila = sim E NÃO superaquecimento | problema_rede_eletrica → cliente_resolve | final |
| DS9 | desliga_sozinho | cheiro_de_queimado = sim | fonte_com_defeito → encaminhar_bancada | final |
| DS10 | desliga_sozinho | tipo_equipamento = notebook E desliga_ao_tirar_carregador = sim | bateria_com_defeito → encaminhar_bancada | final |
| DS11 | desliga_sozinho | tela_azul_antes_de_desligar = sim E instalou_programa_ou_driver_recentemente = sim | problema_software → cliente_resolve | final |
| DS12 | desliga_sozinho | tela_azul_antes_de_desligar = sim E instalou_programa_ou_driver_recentemente = nao E NÃO superaquecimento | problema_memoria_ram → encaminhar_bancada | final |

## 6. Extensões futuras

Sintomas planejados para demonstrar a extensibilidade da base de conhecimento (adicionados apenas editando o arquivo de regras, sem alterar o código):
- Congelamento total do sistema
- Programas fechando sozinhos (como sintoma próprio)

## 7. Como executar

```bash
# [preencher quando houver código]
```

## 8. Testes

[descrever como rodar os testes e quais cenários são validados]

## 9. Integrantes

| Nome completo | Responsabilidade |
|---|---|
| Maria Eduarda Pires | Motor de inferência, módulo de explicação, testes automatizados, regras "não liga", "sistema não inicia" e "lento", integração |
| Luiza Ribeiro | Regras "não carrega" e "internet não conecta", interface e validação de entradas |
| Luciana Tavares | Regras "desliga sozinho", contexto de negócio, cenários de teste, dicionário de regras, roteiro do vídeo e PDF de entrega |

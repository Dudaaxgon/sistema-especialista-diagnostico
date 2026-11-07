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

### Glossário de conclusões intermediárias compartilhadas
Conclusões usadas por regras de mais de um sintoma. **Todas devem usar exatamente estes nomes.** Para criar uma nova, adicione aqui antes de usar.

| Nome | Significado | Usada nos sintomas |
|---|---|---|
| `superaquecimento` | O equipamento está esquentando além do normal | Desliga sozinho, Lento |
| `problema_disco` | Há indícios de falha no disco (HD/SSD) | Sistema não inicia, Lento |
| `alimentacao_externa_ok` | Tomada e carregador/fonte estão funcionando | Não liga, Não carrega |

### Dicionário de regras
| ID | Sintoma | Condições (SE) | Conclusão (ENTÃO) | Tipo |
|---|---|---|---|---|
| R1 | nao_liga | trocou_tomada = sim E funcionou_outra_tomada = sim | tomada_defeituosa → cliente_resolve | final |
| R2 | | | | |

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

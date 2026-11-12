# Divisão de tarefas e cronograma

**Entrega final:** 28/11/2026 às 23:59 (PDF no Teams com link do GitHub + link do vídeo).
**Meta interna:** entregar no dia 27/11, com margem.

> ⚠️ **Regras do trabalho que afetam a nota de TODAS:**
> - Cada pessoa precisa ter **commits próprios** no GitHub. Quem não tiver commits pode ter a nota reduzida (item 1.7.1).
> - No vídeo, **cada pessoa precisa saber explicar QUALQUER parte do código**, inclusive a das outras (itens 2.4 e 2.5). Então todas precisam ler e entender o código todo, não só a sua parte.
> - App que não roda na máquina do professor = **nota zero**.

---

## Status atual (atualizado em 11/11)

- ✅ Regras dos 6 sintomas escritas e no repositório
- ✅ Ajustes nas regras da Luiza aplicados
- ✅ Primeiro commit: 3 de 3 integrantes
- 🔜 Próxima etapa: motor de inferência (Duda), prazo 15/11

---

## Tarefas por pessoa

### Maria Eduarda (Duda)
- [ ] Definir o tipo de encadeamento (para frente ou para trás) e a justificativa
- [x] Escrever as regras dos sintomas **"não liga"**, **"sistema não inicia"** e **"lento, travando ou fechando programas"** (mínimo 6 regras cada)
- [x] Revisar as regras da Luiza e enviar os ajustes necessários
- [ ] Implementar o **motor de inferência**, incluindo condições negadas (ex.: `NÃO problema_disco`) e distinguindo fato falso de fato desconhecido; só avaliar negação após coletar as respostas aplicáveis e concluir as inferências
- [ ] Implementar o **módulo de explicação** ("por quê / como")
- [ ] Implementar os **testes automatizados** a partir dos cenários escritos pela Luciana
- [ ] Converter as regras de todas para o formato final usado pelo código
- [ ] Integrar as partes e revisar o código do grupo
- [ ] Fazer uma **chamada curta explicando o código** para o grupo antes da gravação

### Luiza Ribeiro
- [x] Escrever as regras do sintoma **"não carrega"** (mínimo 6 regras; só notebook; incluir o caso do carregador conectando e desconectando)
- [x] Escrever as regras do sintoma **"internet não conecta"** (mínimo 6 regras)
- [x] Aplicar os ajustes da revisão (fato com espaço no nome, INT-R3, INT-R4, INT-R5, fato sem uso, regras intermediárias, `alimentacao_externa_ok` no "não carrega")
- [ ] Implementar a **interface de perguntas e respostas** (terminal)
- [ ] Implementar o **tratamento de entradas inválidas** e o caso **"não foi possível concluir"**

### Luciana Tavares
- [x] Escrever as regras do sintoma **"desliga sozinho"** (mínimo 6 regras; usar a conclusão `superaquecimento` do glossário)
- [ ] Preencher a seção **"Contexto de negócio"** do README
- [ ] Escrever **cenários de teste** em texto (sem código): para cada sintoma, 2 situações com as respostas do cliente e o diagnóstico esperado
- [ ] Montar o **PDF de entrega** (nomes completos, link do GitHub, link do vídeo)
- [ ] Conferir que o **repositório está público** e que o **link do vídeo está com visualização liberada** (abrir os dois links numa aba anônima para testar)

### Todas
- [x] Fazer pelo menos um commit nesta semana
- [ ] Preencher o **dicionário de regras** do README com as **próprias regras**
- [ ] Montar juntas o **roteiro do vídeo** (10 min, dividindo o tempo entre as três)
- [ ] Usar **exatamente os nomes do glossário** de conclusões intermediárias (seção 5 do README). Para criar uma conclusão compartilhada nova, adicionar no glossário antes de usar
- [ ] Ler e entender o código completo antes da gravação
- [ ] Testar o sistema na própria máquina seguindo o "Como executar" do README
- [ ] Participar da gravação

---

## Como escrever as regras

Use o formato da seção 5 do README. Para cada sintoma:

1. Liste as **causas possíveis** desse problema.
2. Para cada par de causas, pense: **que pergunta separa uma da outra?** Essa pergunta vira uma condição.
3. Procure **conclusões intermediárias**: conclusões que não são o diagnóstico final, mas que outras regras usam (ex.: `superaquecimento`). Confira o glossário antes de inventar um nome novo.
4. Use `tipo_equipamento` como condição **só quando o raciocínio muda** entre notebook e desktop. Não duplique regras.
5. Diferencie **sintoma** (o motivo de o cliente procurar ajuda) de **evidência** (uma pista, como ruído na ventoinha).
6. Escreva as perguntas em **linguagem simples**: quem usa o sistema é o cliente, não um técnico.

**Não escreva como fluxograma** ("primeiro pergunta X, se sim pergunta Y..."). Cada regra deve ser independente: só condições → conclusão.

---

## Cronograma

| Prazo | Entrega | Responsável | Status |
|---|---|---|---|
| **10/11** | Primeiro commit de cada pessoa | Todas | ✅ |
| **11/11** | Regras de "não liga", "não carrega" e "internet não conecta" escritas no formato padrão | Duda, Luiza | ✅ |
| **14/11** | Regras de "sistema não inicia", "lento" e "desliga sozinho" escritas | Duda, Luciana | ✅ |
| **15/11** | Motor de inferência + explicação funcionando com as regras de "não liga" | Duda | 🔄 |
| **16/11** | Contexto de negócio no README + cenários de teste escritos | Luciana | ⏳ |
| **20/11** | Interface, exceções e testes automatizados prontos; todas as regras integradas | Luiza, Duda | ⏳ |
| **22/11** | Dicionário de regras e roteiro do vídeo prontos | Todas | ⏳ |
| **22/11** | Chamada de explicação do código para o grupo | Duda | ⏳ |
| **23/11** | Sistema completo, testado em pelo menos 2 computadores diferentes; README finalizado | Todas | ⏳ |
| **24–26/11** | Gravação do vídeo (entre 9 e 11 minutos) | Todas | ⏳ |
| **27/11** | PDF montado e enviado no Teams | Luciana | ⏳ |

Legenda: ✅ concluído · 🔄 em andamento · ⏳ não iniciado

### Diferenciais (só se sobrar tempo, depois de 20/11)
- [ ] Base de conhecimento em arquivo externo (JSON)
- [ ] Novos sintomas como demonstração de extensibilidade: congelamento e programas fechando sozinhos (depende do JSON)
- [ ] Fatores de certeza nas regras
- [ ] Interface web (Flask ou Streamlit)
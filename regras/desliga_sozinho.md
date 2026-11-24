# Regras — Computador desliga sozinho

Sintoma: `desliga_sozinho`

```
DS1
SE: equipamento_muito_quente = sim
ENTÃO: superaquecimento
TIPO: intermediária
EXPLICAÇÃO: O equipamento está muito quente, o que indica superaquecimento.
```

```
DS2
SE: ventoinha_barulhenta_ou_parada = sim
ENTÃO: superaquecimento
TIPO: intermediária
EXPLICAÇÃO: Ventoinha com barulho forte ou parada não resfria o equipamento, o que pode causar superaquecimento.
```

```
DS3
SE: desliga_em_uso_pesado = sim
E sem_limpeza_ha_mais_de_1_ano = sim
ENTÃO: superaquecimento
TIPO: intermediária
EXPLICAÇÃO: Desligar sob uso pesado em um equipamento sem limpeza há mais de 1 ano indica acúmulo de poeira e superaquecimento.
```

```
DS4
SE: superaquecimento
E tipo_equipamento = notebook
E usa_sobre_cama_ou_sofa = sim
ENTÃO: causa = ventilacao_bloqueada
TIPO: final
AÇÃO: cliente_resolve
EXPLICAÇÃO: O notebook superaquece e é usado sobre superfícies macias, que bloqueiam a saída de ar. Use-o sobre superfície firme.
```

```
DS5
SE: superaquecimento
ENTÃO: causa = limpeza_ou_pasta_termica
TIPO: final
AÇÃO: encaminhar_bancada
EXPLICAÇÃO: Há superaquecimento, e o motivo mais comum é poeira interna ou pasta térmica ressecada, que exigem limpeza técnica.
```

```
DS6
SE: tipo_equipamento = desktop
E desliga_em_uso_pesado = sim
E NÃO superaquecimento
ENTÃO: causa = fonte_insuficiente_ou_defeituosa
TIPO: final
AÇÃO: encaminhar_bancada
EXPLICAÇÃO: O desktop desliga sob uso pesado, mas sem sinais de calor, o que aponta para uma fonte insuficiente ou defeituosa.
```

```
DS7
SE: desliga_ao_mexer_no_cabo_ou_tomada = sim
ENTÃO: causa = mau_contato_energia
TIPO: final
AÇÃO: cliente_resolve
EXPLICAÇÃO: Desligar ao mexer no cabo ou na tomada indica mau contato. Troque o cabo ou a tomada.
```

```
DS8
SE: energia_da_casa_oscila = sim
E NÃO superaquecimento
ENTÃO: causa = problema_rede_eletrica
TIPO: final
AÇÃO: cliente_resolve
EXPLICAÇÃO: A energia da casa oscila e não há sinais de calor, então a rede elétrica é a causa provável. Use estabilizador ou nobreak.
```

```
DS9
SE: cheiro_de_queimado = sim
ENTÃO: causa = fonte_com_defeito
TIPO: final
AÇÃO: encaminhar_bancada
EXPLICAÇÃO: Cheiro de queimado indica falha elétrica. Desligue da tomada e não use até a avaliação técnica.
```

```
DS10
SE: tipo_equipamento = notebook
E desliga_ao_tirar_carregador = sim
ENTÃO: causa = bateria_com_defeito
TIPO: final
AÇÃO: encaminhar_bancada
EXPLICAÇÃO: O notebook desliga assim que o carregador é removido, o que mostra que a bateria não segura carga.
```

```
DS11
SE: tela_azul_antes_de_desligar = sim
E instalou_programa_ou_driver_recentemente = sim
ENTÃO: causa = problema_software
TIPO: final
AÇÃO: cliente_resolve
EXPLICAÇÃO: A tela azul começou depois de instalar um programa ou driver, então o software novo é a causa provável. Desinstale-o.
```

```
DS12
SE: tela_azul_antes_de_desligar = sim
E instalou_programa_ou_driver_recentemente = nao
E NÃO superaquecimento
ENTÃO: causa = problema_memoria_ram
TIPO: final
AÇÃO: encaminhar_bancada
EXPLICAÇÃO: Tela azul sem mudança de software e sem superaquecimento aponta para defeito na memória RAM.
```

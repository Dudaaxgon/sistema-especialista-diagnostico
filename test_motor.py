import unittest

from motor import inferir


def causas(resultados):
    return {(r["causa"], r["acao"]) for r in resultados}


class TestMotorInferencia(unittest.TestCase):
    def test_nao_liga_tomada_defeituosa(self):
        resultados = inferir(
            "nao_liga",
            {"testou_outra_tomada": "sim", "funcionou_outra_tomada": "sim"},
        )
        self.assertIn(("tomada_original_com_problema", "cliente_resolve"), causas(resultados))
        self.assertTrue(resultados[0]["como"].startswith("Regra(s):"))
        self.assertIn("NL-R1", resultados[0]["regras"])

    def test_nao_liga_sem_sinal_com_alimentacao_ok_desktop(self):
        respostas = {
            "tipo_equipamento": "desktop",
            "cabo_energia_conectado": "sim",
            "tomada_funciona": "sim",
            "chave_fonte_ligada": "sim",
            "usa_filtro_linha": "nao",
            "sinal_de_vida": "nao",
        }
        resultados = inferir("nao_liga", respostas)
        self.assertIn(("possivel_falha_interna_energia", "encaminhar_bancada"), causas(resultados))
        texto = " ".join(r["como"] for r in resultados)
        self.assertIn("alimentacao_externa_ok", texto)
        self.assertIn("NL-R10", texto)

    def test_sistema_nao_inicia_problema_disco_por_mensagem(self):
        resultados = inferir(
            "sistema_nao_inicia",
            {"mensagem_disco_nao_encontrado": "sim"},
        )
        self.assertIn(("possivel_falha_disco", "encaminhar_bancada"), causas(resultados))

    def test_sistema_nao_inicia_negacao_exige_fatos_coletados(self):
        # Sem coletar fatos que poderiam provar problema_disco, NÃO problema_disco
        # permanece desconhecido e SNI-R5 não deve disparar.
        resultados = inferir("sistema_nao_inicia", {"reinicia_sem_parar": "sim"})
        self.assertEqual(resultados, [])

        # Com as entradas relevantes respondidas como "nao", a negação pode ser concluída.
        resultados = inferir(
            "sistema_nao_inicia",
            {
                "reinicia_sem_parar": "sim",
                "mensagem_disco_nao_encontrado": "nao",
                "cliques_no_disco": "nao",
            },
        )
        self.assertIn(("possivel_falha_no_sistema", "encaminhar_bancada"), causas(resultados))
        self.assertIn("NÃO problema_disco", resultados[0]["como"])

    def test_lento_superaquecimento_notebook(self):
        resultados = inferir(
            "lento",
            {
                "tipo_equipamento": "notebook",
                "esquenta_muito": "sim",
                "ruido_alto_ventoinha": "sim",
            },
        )
        self.assertIn(("possivel_superaquecimento", "encaminhar_bancada"), causas(resultados))
        self.assertIn("superaquecimento", " ".join(r["como"] for r in resultados))

    def test_lento_pouco_espaco(self):
        resultados = inferir("lento", {"armazenamento_quase_cheio": "sim"})
        self.assertIn(("pouco_espaco_armazenamento", "cliente_resolve"), causas(resultados))

    def test_desliga_sozinho_intermediaria_formato_igual_sim(self):
        # Regras de desliga_sozinho usam "superaquecimento = sim"; o motor deve
        # aceitar conclusões intermediárias derivadas nesse formato.
        resultados = inferir("desliga_sozinho", {"equipamento_muito_quente": "sim"})
        self.assertIn(("limpeza_ou_pasta_termica", "encaminhar_bancada"), causas(resultados))

    def test_multiplos_diagnosticos_ordenados_por_acao(self):
        resultados = inferir(
            "desliga_sozinho",
            {
                "tipo_equipamento": "notebook",
                "equipamento_muito_quente": "sim",
                "usa_sobre_cama_ou_sofa": "sim",
            },
        )
        self.assertEqual(
            [r["acao"] for r in resultados],
            ["encaminhar_bancada", "cliente_resolve"],
        )


if __name__ == "__main__":
    unittest.main()

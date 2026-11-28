import unittest
from unittest.mock import patch

from interface import coletar_respostas, deve_perguntar, executar_interface, ler_opcao
from motor import inferir


class InterfaceTests(unittest.TestCase):
    def test_entrada_invalida_repete_pergunta(self):
        respostas = iter(("talvez", "sim"))
        with patch("builtins.print") as imprimir:
            resultado = ler_opcao("Responda", ("sim", "nao"), lambda _: next(respostas))

        self.assertEqual(resultado, "sim")
        imprimir.assert_called()

    def test_questionario_nao_carrega_coleta_condicionais(self):
        respostas = iter(("notebook", "sim", "nao", "sim", "sim", "sim", "nao", "sim", "nao"))
        fatos = coletar_respostas("nao_carrega", lambda _: next(respostas))

        self.assertEqual(fatos["tipo_equipamento"], "notebook")
        self.assertEqual(fatos["carregador_tem_indicador"], "sim")
        self.assertEqual(fatos["indicador_carregador_aceso"], "sim")
        resultados = inferir("nao_carrega", fatos)
        self.assertIn(
            ("possivel_falha_bateria", "encaminhar_bancada"),
            {(resultado["causa"], resultado["acao"]) for resultado in resultados},
        )
        self.assertIn("carregador_ou_cabo_danificado", fatos)

    def test_questionario_nao_carrega_pula_luz_sem_indicador(self):
        respostas = iter(("notebook", "sim", "nao", "nao", "nao", "sim", "sim", "nao"))
        fatos = coletar_respostas("nao_carrega", lambda _: next(respostas))

        self.assertEqual(fatos["carregador_tem_indicador"], "nao")
        self.assertNotIn("indicador_carregador_aceso", fatos)
        resultados = inferir("nao_carrega", fatos)
        self.assertIn(
            ("possivel_falha_no_carregador_ou_entrada", "encaminhar_bancada"),
            {(resultado["causa"], resultado["acao"]) for resultado in resultados},
        )

    def test_todos_sintomas_possuem_questionario(self):
        from interface import PERGUNTAS, SINTOMAS

        for sintoma, _ in SINTOMAS.values():
            self.assertIn(sintoma, PERGUNTAS)

    def test_pergunta_de_software_so_aparece_apos_tela_azul(self):
        self.assertTrue(
            deve_perguntar(
                "instalou_programa_ou_driver_recentemente",
                {"tela_azul_antes_de_desligar": "sim"},
            )
        )
        self.assertFalse(
            deve_perguntar(
                "instalou_programa_ou_driver_recentemente",
                {"tela_azul_antes_de_desligar": "nao"},
            )
        )

    def test_informacoes_insuficientes_exibem_mensagem(self):
        with patch("builtins.print") as imprimir:
            executar_interface(
                lambda _sintoma, _respostas: [],
                lambda prompt: (
                    "1"
                    if "número" in prompt
                    else "notebook"
                    if "O equipamento é" in prompt
                    else "nao"
                ),
            )

        mensagens = [call.args[0] for call in imprimir.call_args_list if call.args]
        self.assertTrue(any("Não foi possível concluir" in str(m) for m in mensagens))

    def test_motor_reconhece_sintoma_desliga_sozinho(self):
        resultados = inferir(
            "desliga_sozinho",
            {
                "tipo_equipamento": "notebook",
                "equipamento_muito_quente": "sim",
                "usa_sobre_cama_ou_sofa": "sim",
            },
        )
        causas = {resultado["causa"] for resultado in resultados}
        self.assertIn("limpeza_ou_pasta_termica", causas)
        self.assertIn("ventilacao_bloqueada", causas)


if __name__ == "__main__":
    unittest.main()

"""Testes de contrato da geração e integração com a CLI."""

from pathlib import Path
import string
import subprocess
import sys
import unittest
from unittest.mock import patch

from gerador import gerar_senha


SCRIPT = Path(__file__).resolve().parents[1] / "gerador.py"
SIMBOLOS = "!@#$%&*+-=?_"


class TestGerador(unittest.TestCase):
    def assert_criterios(self, senha, tamanho, simbolos=True):
        self.assertEqual(len(senha), tamanho)
        grupos = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
        if simbolos:
            grupos.append(SIMBOLOS)
        self.assertTrue(set(senha) <= set("".join(grupos)))
        for grupo in grupos:
            self.assertTrue(any(c in grupo for c in senha))

    def test_padrao_de_vinte_caracteres(self):
        self.assert_criterios(gerar_senha(), 20)

    def test_tamanhos_e_limites(self):
        for tamanho in (8, 16, 24, 64, 256):
            with self.subTest(tamanho=tamanho):
                self.assert_criterios(gerar_senha(tamanho), tamanho)

    def test_sem_simbolos(self):
        for tamanho in (8, 20, 256):
            with self.subTest(tamanho=tamanho):
                self.assert_criterios(gerar_senha(tamanho, False), tamanho, False)

    def test_tamanhos_invalidos(self):
        for tamanho in (-1, 0, 7, 257):
            with self.subTest(tamanho=tamanho):
                with self.assertRaises(ValueError):
                    gerar_senha(tamanho)

    def test_descarta_candidata_sem_tipo_obrigatorio(self):
        # Primeira candidata inválida, segunda válida; não depende de sorte.
        with patch("gerador.secrets.choice", side_effect=list("aaaaaaaaAa1!bcde")):
            self.assertEqual(gerar_senha(8), "Aa1!bcde")

    def test_falha_da_fonte_aleatoria_nao_gera_fallback(self):
        with patch("gerador.secrets.choice", side_effect=OSError("fonte indisponível")):
            with self.assertRaises(OSError):
                gerar_senha()


class TestCLI(unittest.TestCase):
    def executar(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args], capture_output=True,
            text=True, encoding="utf-8", errors="replace", timeout=10,
        )

    def test_execucao_padrao(self):
        resultado = self.executar()
        self.assertEqual(resultado.returncode, 0)
        self.assertEqual(resultado.stderr, "")
        self.assertEqual(len(resultado.stdout.strip()), 20)
        self.assertEqual(len(resultado.stdout.splitlines()), 1)

    def test_opcoes_de_tamanho_e_simbolos(self):
        resultado = self.executar("--tamanho", "24", "--sem-simbolos")
        self.assertEqual(resultado.returncode, 0)
        senha = resultado.stdout.strip()
        self.assertEqual(len(senha), 24)
        self.assertTrue(set(senha) <= set(string.ascii_letters + string.digits))

    def test_tamanho_fora_do_intervalo(self):
        resultado = self.executar("-t", "7")
        self.assertEqual(resultado.returncode, 2)
        self.assertEqual(resultado.stdout, "")
        self.assertIn("8 e 256", resultado.stderr)

    def test_tamanho_nao_numerico(self):
        resultado = self.executar("-t", "abc")
        self.assertEqual(resultado.returncode, 2)
        self.assertEqual(resultado.stdout, "")

    def test_opcao_desconhecida(self):
        resultado = self.executar("--inexistente")
        self.assertEqual(resultado.returncode, 2)
        self.assertEqual(resultado.stdout, "")

    def test_ajuda(self):
        resultado = self.executar("--help")
        self.assertEqual(resultado.returncode, 0)
        self.assertIn("--tamanho", resultado.stdout)
        self.assertIn("--sem-simbolos", resultado.stdout)


if __name__ == "__main__":
    unittest.main()

from project.core import saudacao

def test_saudacao():
    assert saudacao("Mundo") == "Olá, Mundo! Bem-vindo à nossa biblioteca."

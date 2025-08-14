# tests/test_cli.py
# corre com pytest -v tests/test_cli.py
import pytest
from gestor.cli import main

def test_add_movimento_stdout(capsys):
    argv = [
        "add-mov",
        "--data", "2025-08-14",
        "--valor", "100.50",
        "--categoria", "Alimentação",
        "--tipo", "despesa",
        "--descricao", "Compras supermercado",
        "--metodo", "cartão"
    ]
    
    main(argv)
    
    captured = capsys.readouterr()
    assert "Criado movimento" in captured.out
    assert "Alimentação" in captured.out
    assert "100.5" in captured.out  # valor impresso

def test_add_movimento_invalid_tipo():
    argv = [
        "add-mov",
        "--data", "2025-08-14",
        "--valor", "50",
        "--categoria", "Alimentação",
        "--tipo", "errado"  # tipo inválido
    ]
    
    with pytest.raises(SystemExit):  # argparse termina o programa com SystemExit
        main(argv)
def test_add_orcamento_default_periodo(capsys):
    argv = [
        "add-orc",
        "--categoria", "Lazer",
        "--limite", "200"
    ]
    
    main(argv)
    captured = capsys.readouterr()
    assert "Lazer" in captured.out
    assert "(mensal)" in captured.out  # default período

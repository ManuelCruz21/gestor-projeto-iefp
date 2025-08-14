# tests/test_orc.py
# Corre com: pytest -v tests/test_orc.py


import pytest
from gestor.models import Orcamento, PERIODO

def test_orcamento_valido():
    o = Orcamento(
        id_=1,
        categoria="Alimentação",
        limite=500,
        periodo="mensal"
    )
    o.validar()
    d = o.to_dict()
    o2 = Orcamento.from_dict(d)
    assert o2.id == 1
    assert o2.categoria == "Alimentação"
    assert o2.limite == 500
    assert o2.periodo == "mensal"

def test_categoria_vazia():
    with pytest.raises(ValueError) as excinfo:
        Orcamento(
            id_=2,
            categoria=" ",
            limite=100,
            periodo="mensal"
        ).validar()
    assert "categoria" in str(excinfo.value).lower()

def test_limite_negativo():
    with pytest.raises(ValueError) as excinfo:
        Orcamento(
            id_=3,
            categoria="Transporte",
            limite=-50,
            periodo="mensal"
        ).validar()
    assert "limite" in str(excinfo.value).lower()

def test_periodo_default():
    # Se não passar periodo, deve usar "mensal"
    o = Orcamento(
        id_=5,
        categoria="Saúde",
        limite=150
    )
    assert o.periodo == "mensal"

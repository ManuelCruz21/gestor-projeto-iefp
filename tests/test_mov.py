# tests/test_mov.py
# Corre com: pytest -v tests/test_mov.py

import pytest
from gestor.models import Movimento, TipoMovimento

def test_movimento_valido():
    m = Movimento(
        id_=1,
        data="2025-08-14",
        valor=100.50,
        categoria="Alimentação",
        tipo=TipoMovimento.Despesa.value,
        descricao="Compras supermercado",
        metodo_de_pagamento="cartão"
    )
    # Não deve levantar exceção
    m.validar()
    d = m.to_dict()
    m2 = Movimento.from_dict(d)
    assert m2.id == 1
    assert m2.categoria == "Alimentação"
    assert m2.tipo == TipoMovimento.Despesa.value
    assert m2.valor == 100.50

def test_categoria_vazia():
    with pytest.raises(ValueError, match="categoria"):
        Movimento(
            id_=2,
            data="2025-08-14",
            valor=50,
            categoria=" ",
            tipo=TipoMovimento.Despesa.value
        ).validar()

def test_tipo_invalido():
    with pytest.raises(ValueError, match="Tipo inválido"):
        Movimento(
            id_=3,
            data="2025-08-14",
            valor=50,
            categoria="Alimentação",
            tipo="errado"
        ).validar()


def test_valor_negativo():
    with pytest.raises(ValueError, match="valor não pode ser negativo"):
        Movimento(
            id_=5,
            data="2025-08-14",
            valor=-10,
            categoria="Alimentação",
            tipo=TipoMovimento.Despesa.value
        ).validar()

# tests/test_service.py
# Corre com: pytest -v tests/test_service.py

import pytest
from gestor.service import GestorService, GestorError


# Mock do Storage em memória
class MockStorage:
    def __init__(self):
        self.movimentos = []
        self.orcamentos = []
        self.relatorios_mov = []
        self.relatorios_orc = []

    def proximo_id(self):
        return len(self.movimentos) + 1

    def proximo_id_orcamentos(self):
        return len(self.orcamentos) + 1

    def carregar_movimentos(self):
        return self.movimentos

    def guardar_movimentos(self, movimentos_lista):
        self.movimentos = movimentos_lista

    def carregar_orcamentos(self):
        return self.orcamentos

    def guardar_orcamentos(self, orcamentos_lista):
        self.orcamentos = orcamentos_lista

    def anexar_relatorio_movimento(self, linha_dict):
        self.relatorios_mov.append(linha_dict)

    def anexar_relatorio_orcamento(self, linha_dict):
        self.relatorios_orc.append(linha_dict)

    def ler_relatorios_movimento(self):
        return self.relatorios_mov

    def ler_relatorios_orcamento(self):
        return self.relatorios_orc


def test_add_movimento_valido():
    storage = MockStorage()
    service = GestorService(storage)

    m = service.add_movimento(
        data="2025-08-14",
        valor=100.0,
        categoria="Alimentação",
        tipo="despesa",
        descricao="Supermercado",
        metodo_de_pagamento="cartão"
    )

    assert m.valor == 100.0
    assert len(storage.movimentos) == 1
    assert len(storage.relatorios_mov) == 1


def test_add_movimento_overspend():
    storage = MockStorage()
    service = GestorService(storage)
    # Criar orçamento mensal de 50
    service.add_orcamento("Alimentação", 50, "mensal")

    # Tentativa de adicionar despesa maior que limite
    with pytest.raises(GestorError, match="ultrapassa o orçamento"):
        service.add_movimento(
            data="2025-08-14",
            valor=100.0,
            categoria="Alimentação",
            tipo="despesa"
        )


def test_listar_movimento_com_filtros():
    storage = MockStorage()
    service = GestorService(storage)
    service.add_movimento("2025-08-14", 100, "Alimentação", "despesa")
    service.add_movimento("2025-08-15", 200, "Transporte", "despesa")
    
    filtrados = service.listar_movimento(filtros={"categoria": "Alimentação"})
    assert len(filtrados) == 1
    assert filtrados[0].categoria == "Alimentação"


def test_add_orcamento_valido():
    storage = MockStorage()
    service = GestorService(storage)

    o = service.add_orcamento("Transporte", 300, "mensal")
    assert o.limite == 300
    assert len(storage.orcamentos) == 1
    assert len(storage.relatorios_orc) == 1


def test_verificar_overspend():
    storage = MockStorage()
    service = GestorService(storage)
    service.add_orcamento("Alimentação", 100, "mensal")
    assert service.verificar_overspend("Alimentação", 50) is False
    assert service.verificar_overspend("Alimentação", 200) is True


def test_relatorios():
    storage = MockStorage()
    service = GestorService(storage)

    # adicionar orcamento e movimentos
    service.add_orcamento("Alimentação", 100)
    service.add_movimento("2025-08-14", 60, "Alimentação", "despesa")
    service.add_movimento("2025-08-15", 40, "Alimentação", "receita")

    tot_por_cat = service.relatorio_valores_totais_mov_por_categoria()
    assert tot_por_cat[0][0] == "Alimentação"
    assert tot_por_cat[0][1] == 100

    cashflow = service.relatorio_cashflow_semanal()
    assert len(cashflow) == 1
    assert cashflow[0][2] == 40  # receita
    assert cashflow[0][3] == 60  # despesa
    assert cashflow[0][4] == -20 # saldo

    top_cats = service.relatorio_top_categorias()
    assert top_cats[0][0] == "Alimentação"
    assert top_cats[0][1] == 100

    alertas = service.relatorio_alertas()
    assert alertas[0][0] == "Alimentação"
    assert alertas[0][1] == 100
    assert alertas[0][2] == 60
    assert alertas[0][3] == 0 

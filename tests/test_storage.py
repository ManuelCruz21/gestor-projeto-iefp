#tests/test_storage.py
# Corre com: pytest -v tests/test_storage.py

import pytest
import os
from gestor.storage import Storage

@pytest.fixture
def storage(tmp_path):
    """Instancia Storage com pasta temporária."""
    return Storage(tmp_path)

def test_movimentos_guardar_carregar(storage):
    movs = [{"id":1,"data":"2025-08-14","valor":100,"categoria":"A","tipo":"despesa","descricao":"","metodo_de_pagamento":"dinheiro"}]
    storage.guardar_movimentos(movs)
    carregado = storage.carregar_movimentos()
    assert carregado == movs

def test_proximo_id(storage):
    assert storage.proximo_id() == 1
    storage.guardar_movimentos([{"id":1}])
    assert storage.proximo_id() == 2

def test_orcamentos_guardar_carregar(storage):
    orcs = [{"id":1,"categoria":"Lazer","limite":100,"periodo":"mensal"}]
    storage.guardar_orcamentos(orcs)
    carregado = storage.carregar_orcamentos()
    assert carregado == orcs

def test_proximo_id_orcamentos(storage):
    assert storage.proximo_id_orcamentos() == 1
    storage.guardar_orcamentos([{"id":3}])
    assert storage.proximo_id_orcamentos() == 4

def test_anexar_relatorio_movimento(storage):
    linha = {"id":1,"data":"2025-08-14","valor":50,"categoria":"A","tipo":"despesa","descricao":"","metodo_de_pagamento":"dinheiro"}
    storage.anexar_relatorio_movimento(linha)
    relatorio = storage.ler_relatorios_movimento()
    assert len(relatorio) == 1
    assert relatorio[0]["id"] == '1'  # CSV lê tudo como string

def test_anexar_relatorio_orcamento(storage):
    linha = {"id":1,"categoria":"Lazer","limite":100,"periodo":"mensal"}
    storage.anexar_relatorio_orcamento(linha)
    relatorio = storage.ler_relatorios_orcamento()
    assert len(relatorio) == 1
    assert relatorio[0]["categoria"] == "Lazer"

def test_carregar_movimentos_vazio(storage):
    assert storage.carregar_movimentos() == []

def test_carregar_orcamentos_vazio(storage):
    assert storage.carregar_orcamentos() == []

def test_ler_relatorios_movimento_vazio(storage):
    assert storage.ler_relatorios_movimento() == []

def test_ler_relatorios_orcamento_vazio(storage):
    assert storage.ler_relatorios_orcamento() == []

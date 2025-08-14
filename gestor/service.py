#gestor/service.py

from .models import Movimento,Orcamento
from .storage import Storage

class GestorError(Exception):
    pass

class GestorService:

    def __init__(self,storage):
        self.storage = storage

    def add_movimento(self, data, valor, categoria,tipo,descricao="",metodo_de_pagamento="dinheiro"):
      
        novo_id = self.storage.proximo_id()
        movimento = Movimento(novo_id,data,valor,categoria,tipo,descricao,metodo_de_pagamento)
        movimento.validar()

        if tipo == "despesa" and self.verificar_overspend(categoria,valor):
            raise GestorError("O valor ultrapassa o orçamento!")

        movimentos = self.storage.carregar_movimentos()
        movimentos.append(movimento.to_dict())
        self.storage.guardar_movimentos(movimentos)
        return movimento
    
    def listar_movimento(self):
        #carregar dicionarios e converter para objeto Movimentos (só para fazer a impressão mais organizada)
        return [Movimento.from_dict(d) for d in self.storage.carregar_movimentos()]
    
    def add_orcamento(self, categoria, limite, periodo="mensal"):
        novo_id = self.storage.proximo_id_orcamentos()
        orcamento = Orcamento(novo_id, categoria, limite, periodo)
        orcamento.validar()
        orcamentos = self.storage.carregar_orcamentos()
        orcamentos.append(orcamento.to_dict())  # garante dicionário
        self.storage.guardar_orcamentos(orcamentos)
        return orcamento

    
    def listar_orcamento(self,periodo=None):
        #carregar dicionarios e converter para objeto Orcamento (só para fazer a impressão mais organizada)
        orcamentos_dict = self.storage.carregar_orcamentos()
        orcamentos = [Orcamento.from_dict(o) for o in orcamentos_dict]
        if periodo:
            orcamentos = [o for o in orcamentos if o.periodo == periodo]
        return orcamentos

    def verificar_overspend(self, categoria, valor_despesa):
        # Carregar orçamentos mensais para a categoria
        orcamentos = self.listar_orcamento(periodo="mensal")
        for o in orcamentos:
            if o.categoria == categoria and valor_despesa > o.limite:
                return True
        return False
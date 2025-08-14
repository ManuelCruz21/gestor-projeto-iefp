#gestor/service.py

from .models import Movimento
from .storage import Storage

class GestorService:

    def __init__(self,storage):
        self.storage = storage

    def add_movimento(self, data, valor, categoria,tipo,descricao="",metodo_de_pagamento="dinheiro"):
        
        novo_id = self.storage.proximo_id()
        movimento = Movimento(novo_id,data,valor,categoria,tipo,descricao,metodo_de_pagamento)
        movimento.validar()
        movimentos = self.storage.carregar_movimentos()
        movimentos.append(movimento.to_dict())
        self.storage.guardar_movimentos(movimentos)

        return movimento
    
    def listar_movimento(self):
        #carregar dicionarios e converter para objeto Movimentos (só para fazer a impressão mais organizada)
        return [Movimento.from_dict(d) for d in self.storage.carregar_movimentos()]
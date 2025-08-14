#gestor/models.py
#Criar classes e validar com if/raise

#Para se utilizar a Enumeração
from enum import Enum
#Para se poder colocar no formato ISO (YYYY-MM-DD)
from datetime import datetime

METODOS_VALIDOS = ["dinheiro", "cartão", "transferência"]


class TipoMovimento(Enum):
    #Escolha de string em vez de int para uma leitura mais legível
    Despesa = "despesa"
    Receita = "receita"


class Movimento:
    # construtor e os seus vários metodos

    def __init__(self, id_, data, valor, categoria, tipo,descricao="",metodo_de_pagamento="dinheiro"):
        self.id = id_
        self.data = datetime.fromisoformat(data)
        self.valor = float(valor)
        self.categoria = str(categoria)
        self.tipo = tipo
        self.descricao = str(descricao)
        self.metodo_de_pagamento = metodo_de_pagamento if metodo_de_pagamento in METODOS_VALIDOS else "dinheiro"

    def validar(self):
        #garantir que os dados básicos estão corretos e dentro dos parametros pretendidos
        if not self.categoria.strip():
            raise ValueError("A categoria é obrigatório")
        if self.tipo not in (t.value for t in TipoMovimento):
            raise ValueError(f"Tipo inválido: {self.tipo}")
        if self.metodo_de_pagamento not in METODOS_VALIDOS:
            raise ValueError(f"Método de pagamento inválido: {self.metodo_de_pagamento}")
        if self.valor < 0:
            raise ValueError("O valor não pode ser negativo.")
    
    def to_dict(self):
        #converter o objeto movimento em dicionário para guardar em JSON
        return{
            "id":self.id,
            "data":self.data.isoformat(),
            "valor":self.valor,
            "categoria":self.categoria,
            "tipo":self.tipo,
            "descricao":self.descricao,
            "método de pagamento":self.metodo_de_pagamento
        }
    
    def from_dict(d):
        #criar o objeto movimento a partir do dicionario (Quando carregamos o ficheiro JSON)
        return Movimento(
            id_= int(d["id"]),
            data=d.get("data", datetime.now().isoformat()),
            valor = float(d.get("valor",0.0)),
            categoria = d.get("categoria", ""),
            tipo = d.get("tipo", ""),
            descricao= d.get("descricao", ""),
            metodo_de_pagamento=d.get("método de pagamento", "dinheiro")
        )

#gestor/service.py

from .models import Movimento,Orcamento,calcular_semana
from .storage import Storage
from datetime import datetime

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
        
        self.storage.anexar_relatorio({
            "id": novo_id,
            "data": datetime.now().isoformat(),
            "valor": valor,
            "categoria": categoria,
            "tipo": tipo,
            "descricao": descricao,
            "metodo_de_pagamento": metodo_de_pagamento
            })

        movimentos = self.storage.carregar_movimentos()
        movimentos.append(movimento.to_dict())
        self.storage.guardar_movimentos(movimentos)

        return movimento
    
    def listar_movimento(self,filtros=None):
        filtros=filtros or {}
        todos = [Movimento.from_dict(d) for d in self.storage.carregar_movimentos()]
        def passa(m):
            if filtros.get("categoria") and (m.categoria) != (filtros["categoria"]):
                return False
            if filtros.get("tipo") and m.tipo != filtros["tipo"]:
                return False
            if filtros.get("data") and m.data != datetime.fromisoformat(filtros["data"]):
                return False
            if filtros.get("descricao") and filtros["descricao"].lower() not in m.descricao.lower():
                return False
            return True
        #carregar dicionarios e converter para objeto Movimentos (só para fazer a impressão mais organizada)
        return [m for m in todos if passa(m)]

    
    def add_orcamento(self, categoria, limite, periodo="mensal"):
        novo_id = self.storage.proximo_id_orcamentos()
        orcamento = Orcamento(novo_id, categoria, limite, periodo)
        orcamento.validar()

        self.storage.anexar_relatorio_orcamento({
            "id": novo_id,
            "limite":limite,
            "categoria": categoria,
            "periodo":periodo,
        })
        
        orcamentos = self.storage.carregar_orcamentos()
        orcamentos.append(orcamento.to_dict())  # garante dicionário
        self.storage.guardar_orcamentos(orcamentos)
        return orcamento

    
    def listar_orcamento(self,filtros=None):
        #carregar dicionarios e converter para objeto Orcamento (só para fazer a impressão mais organizada)
        filtros = filtros or {}
        todos = [Orcamento.from_dict(o) for o in self.storage.carregar_orcamentos()]
        def passa(o):
            if filtros.get("periodo") and o.periodo != filtros["periodo"]:
                return False
            return True
        return [o for o in todos if passa(o)]

    def verificar_overspend(self, categoria, valor_despesa):
        # Carregar orçamentos mensais para a categoria
        orcamentos = self.listar_orcamento(filtros={"periodo":"mensal"})
        for o in orcamentos:
            if o.categoria == categoria and valor_despesa > o.limite:
                return True
        return False

    #relatórios
    #relatórios de valores totais dos movimentos por categoria
    def relatorio_valores_totais_mov_por_categoria(self):
        #ler as sessões do csv e somar os valores totais agrupadas pela categoria
        movimentos = self.storage.ler_relatorios_movimento()
        valores_totais = {}
        for m in movimentos:
            categoria = m.get("categoria", "DESCONHECIDO")
            valor = float(m.get("valor",0.0))
            valores_totais[categoria]=valores_totais.get(categoria,0.0) + valor
            #devovler lista com pares ordenada por valores totais de movimentos.
        return sorted(valores_totais.items(),key=lambda x:x[1], reverse=True)
    
    #relatorio de cashflow semanal
    def relatorio_cashflow_semanal(self):
        movimentos = self.storage.ler_relatorios_movimento()  
        semanas = {}

        for m in movimentos:
            data_dt = datetime.fromisoformat(m["data"])
            inicio, fim = calcular_semana(data_dt.isoformat())
            semana = (inicio, fim)
            if semana not in semanas:
                semanas[semana] = {"receita": 0.0, "despesa": 0.0}
        
            if m["tipo"] == "receita":
                semanas[semana]["receita"] += float(m["valor"])
            else:
                semanas[semana]["despesa"] += float(m["valor"])
        
        relatorio = []
        for (inicio, fim), valores in semanas.items():
            saldo = valores["receita"] - valores["despesa"]
            relatorio.append((inicio,   fim, valores["receita"], valores["despesa"], saldo))

        return sorted(relatorio, key=lambda x: x[0])

    #relatorio de top categorias
    def relatorio_top_categorias(self):
        relatorios=self.storage.ler_relatorios_movimento()
        total={}
        for r in relatorios:
            cat = r["categoria"]
            valor = float((r["valor"]))
             # somar ao total da categoria
            total[cat] = total.get(cat, 0.0) + valor
         # ordenar por valor total (descendente)
        top_categorias = sorted(total.items(), key=lambda x: x[1], reverse=True)

        return top_categorias[:5] 

    # relatório de alertas de orçamento
    def relatorio_alertas(self):
        relatorios = self.storage.ler_relatorios_orcamento()  
        limites = {r["categoria"]: float(r["limite"]) for r in relatorios}
        movimentos = self.storage.carregar_movimentos()
        gastos = {}
        for m in movimentos:
            cat = m["categoria"]
            if m["tipo"] == "despesa":
                gastos[cat] = gastos.get(cat, 0.0) + m["valor"]

        relatorio = []
        for categoria, limite in limites.items():
            gasto = gastos.get(categoria, 0.0)
            excesso = gasto - limite if gasto > limite else 0.0
            relatorio.append((categoria, limite, gasto, excesso))

        return relatorio

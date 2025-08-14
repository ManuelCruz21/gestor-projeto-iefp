#gestor/storage.py
#Responsavel por ler e guardar os movimentos e orçamentos em ficheiro JSON assim como exportar relatorios em JSON e CSV.

#importar funcionalidades do sistema operativo para permitir a utilização de pastas, ficheiros e variaveis de ambiente.
import os

# Permite trabalhar com dados em formato JSON, para ler e guardar listas de objetos.
import json, csv

class Storage:

    def __init__(self, base_dir):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        
        # Caminho para o ficheiro JSON onde se guardam os movimentos.
        self.movimentos_path=os.path.join(self.base_dir,"movimentos.json")

        # Caminho para o ficheiro CSV onde se guardam os relatorios 
        self.relatorios_mov_csv=os.path.join(self.base_dir, "relatorios_mov.csv")

        # Caminho para o ficheiro JSON onde se guardam os orçamentos.
        self.orcamentos_path=os.path.join(self.base_dir,"orcamentos.json")

        # Caminho para o ficheiro CSV onde se guardam os orçamentos
        self.relatorios_orc_csv=os.path.join(self.base_dir, "relatorios_orc.csv")
        
    def carregar_movimentos(self):
        #Devolver uma lista de dicionários
        # Se o ficheiro não existir deve devolver uma lista vazia
        if not os.path.exists(self.movimentos_path):
            return []
        with open(self.movimentos_path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def guardar_movimentos(self, movimentos_lista):
        #receber lista de dicionário e gravar em JSON
        with open(self.movimentos_path,"w",encoding="utf-8") as f:
            json.dump(movimentos_lista,f,ensure_ascii=False,indent=2)

    def proximo_id(self):
        #calcular o proximo id com base no maior id já existente
        movimentos = self.carregar_movimentos()
        max_id = 0

        for m in movimentos:
            if int(m.get("id",0)) > max_id:
                max_id = int (m["id"])
        return max_id + 1     
    
    def carregar_orcamentos(self):
        #Devolver uma lista de dicionários
        # Se o ficheiro não existir deve devolver uma lista vazia
        if not os.path.exists(self.orcamentos_path):
            return []
        with open(self.orcamentos_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def guardar_orcamentos(self, orcamentos_lista):
        #receber lista de dicionário e gravar em JSON
        with open(self.orcamentos_path,"w",encoding="utf-8") as f:
            json.dump(orcamentos_lista,f,ensure_ascii=False,indent=2)

    def proximo_id_orcamentos(self):
        #calcular o proximo id com base no maior id já existente
        orcamentos = self.carregar_orcamentos()
        max_id = 0

        for m in orcamentos:
            if int(m.get("id",0)) > max_id:
                max_id = int (m["id"])
        return max_id + 1        
    
    #relatorios CSV - MOVIMENTOS
    def anexar_relatorio_movimento(self,linha_dict):
        #escrever uma linha no CSV; criar cabeçalhos se ainda não existem
        write_header = not os.path.exists(self.relatorios_mov_csv)
        with open(self.relatorios_mov_csv,"a",newline="",encoding="utf-8") as f:
            writer = csv.DictWriter(f,fieldnames=["id","data","valor","categoria","tipo","descricao","metodo_de_pagamento"])
            if write_header:
                writer.writeheader()
            writer.writerow(linha_dict)
    
    #permite ler os relatorios anexados em CSV
    def ler_relatorios_movimento(self):
        if not os.path.exists(self.relatorios_mov_csv):
            #retorna vazio se o ficheiro nao existe
            return[]
        #se o ficheiro exsite, lê o conteudo
        with open(self.relatorios_mov_csv,"r",encoding="utf-8") as f:
            return list(csv.DictReader(f))

    #relatorios CSV - ORCAMENTOS
    def anexar_relatorio_orcamento (self,linha_dict):
        #escrever uma linha no CSV; criar cabeçalhos se ainda não existem
        write_header = not os.path.exists(self.relatorios_orc_csv)
        with open(self.relatorios_orc_csv,"a",newline="",encoding="utf-8") as f:
            writer = csv.DictWriter(f,fieldnames=["id","categoria", "limite", "periodo"])
            if write_header:
                writer.writeheader()
            writer.writerow(linha_dict)
    
    #permite ler os relatorios anexados em CSV
    def ler_relatorios_orcamento(self):
        if not os.path.exists(self.relatorios_orc_csv):
            #retorna vazio se o ficheiro nao existe
            return[]
        #se o ficheiro exsite, lê o conteudo
        with open(self.relatorios_orc_csv,"r",encoding="utf-8") as f:
            return list(csv.DictReader(f))
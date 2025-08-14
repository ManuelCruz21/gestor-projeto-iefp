#gestor/cli.py
#Ler comandos e argumentos no terminal e realizar os pedidos
#O argparse permite passagem de argumentos num comando no terminal

import os, argparse
from .storage import Storage
from .service import GestorService

BASE_DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)),"data")

def build_service():
    return GestorService(Storage(BASE_DATA))

def cmd_add_movimento(args):
    s = build_service()
    m = s.add_movimento(
        data=args.data,
        valor=args.valor,
        categoria=args.categoria,
        tipo=args.tipo,
        descricao=args.descricao or "",
        metodo_de_pagamento=args.metodo,
    )
    
    print(f'Criado movimento #{m.id}: {m.data}, {m.tipo}, {m.categoria}, {m.descricao}, {m.valor}, {m.metodo_de_pagamento}')


def cmd_listar(args):
    s=build_service()
    for m in s.listar_movimento():
        print(f'##{m.id}: {m.data}, {m.tipo}, {m.categoria} - {m.descricao} : {m.valor}€, {m.metodo_de_pagamento}')

def main(argv=None):
    parser = argparse.ArgumentParser(prog="gestor", description= "Gestor de Despesas e Orçamentos (Entrega 1)")
    #funcao para criar movimento
    sub = parser.add_subparsers(required=True)
    p_add= sub.add_parser("add-mov", help="Adicionar novo movimento")
    p_add.add_argument("--data", required=True, help="Data no formato ISO (YYYY-MM-DD)")
    p_add.add_argument("--valor", required=True, type=float, help="Valor do movimento")
    p_add.add_argument("--categoria", required=True, help="Categoria do movimento")
    p_add.add_argument("--tipo", required=True, choices=["despesa", "receita"], help="Tipo do movimento")
    p_add.add_argument("--descricao", default="", help="Descrição do movimento")
    p_add.add_argument("--metodo", choices=["dinheiro", "cartão", "transferência"], default="dinheiro", help="Método de pagamento")
    p_add.set_defaults(func=cmd_add_movimento)

    #funcao para listar tarefa
    p_list = sub.add_parser("list-mov", help="Listar Movimentos")
    p_list.set_defaults(func=cmd_listar)
    args = parser.parse_args(argv)
    args.func(args)

if __name__== "__main__":
    main()

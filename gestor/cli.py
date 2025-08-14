#gestor/cli.py
#Ler comandos e argumentos no terminal e realizar os pedidos
#O argparse permite passagem de argumentos num comando no terminal

import os, argparse
from .storage import Storage
from .service import GestorService
from datetime import datetime

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
    s = build_service()
    filtros = {
        "categoria": args.categoria,
        "tipo": args.tipo,
        "data": args.data,
        "descricao": args.descricao
    }
    movimentos = s.listar_movimento(filtros)

    for m in movimentos:
        print(f'##{m.id}: {m.data}, {m.tipo}, {m.categoria} - {m.descricao} : {m.valor}€, {m.metodo_de_pagamento}')


def cmd_add_orcamento(args):
    s = build_service()
    o = s.add_orcamento(
        categoria=args.categoria,
        limite=args.limite,
        periodo=args.periodo,
    )
    print(f"Orçamento criado: {o.categoria} - {o.limite}€ ({o.periodo})")

def cmd_list_orcamentos(args):
    s = build_service()
    filtros={
        "periodo": args.periodo,
    }
    orcamentos = s.listar_orcamento(filtros)

    for o in orcamentos:
        print(f"#{o.id}: {o.categoria} - {o.limite}€ ({o.periodo})")

def cmd_relatorio(args):
    s=build_service()
    if args.categoria == "totais-por-cat":
        for categoria,total in s.relatorio_valores_totais_mov_por_categoria():
            print(f'{categoria}: {total}€')
    elif args.categoria == "cashflow-semanal":
        for inicio, fim, receita, despesa, saldo in s.relatorio_cashflow_semanal():
            print(f"{inicio} a {fim} | Receita: {receita:.2f}€ | Despesa: {despesa:.2f}€ | Saldo: {saldo:.2f}€")

    elif args.categoria == "top-categorias":
        for categoria, total in s.relatorio_top_categorias():
            print(f"{categoria} - {total:.2f}€")
    elif args.categoria == "alertas":
        for categoria, limite, gasto, excesso in s.relatorio_alertas():
            print(f"{categoria} | Limite: {limite:.2f}€ | Gasto: {gasto:.2f}€ | Excesso: {excesso:.2f}€")
    else:
        print("Tipo de relatório inválido")

def main(argv=None):
    parser = argparse.ArgumentParser(prog="gestor", description= "Gestor de Despesas e Orçamentos (Entrega 2)")
    
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

    #funcao para listar movimento
    p_list = sub.add_parser("list-mov", help="Listar Movimentos")
    p_list.add_argument("--categoria", help="Filtrar por categoria")
    p_list.add_argument("--tipo", choices=["despesa", "receita"], help="Filtrar por tipo")
    p_list.add_argument("--data", help="Filtrar por data (YYYY-MM-DD)")
    p_list.add_argument("--descricao", help="Filtrar por descrição")
    p_list.set_defaults(func=cmd_listar)

    #funcao para criar orcamento
    p_add_orc = sub.add_parser("add-orc", help="Adicionar orçamento")
    p_add_orc.add_argument("--categoria", required=True)
    p_add_orc.add_argument("--limite", type=float, required=True)
    p_add_orc.add_argument("--periodo", choices=["mensal", "anual", "semanal"], default="mensal")
    p_add_orc.set_defaults(func=cmd_add_orcamento)

    #funcao para listar orcamentos
    p_list_orc = sub.add_parser("list-orc", help="Listar orçamentos")
    p_list_orc.add_argument("--periodo", choices=["mensal", "anual", "semanal"])
    p_list_orc.set_defaults(func=cmd_list_orcamentos)

    #funcao para chamar relatorios
    p_rel = sub.add_parser("relatorio", help="Gerar relatórios")
    p_rel.add_argument("--categoria", required=True, choices=["totais-por-cat","cashflow-semanal","top-categorias","alertas"])
    p_rel.set_defaults(func=cmd_relatorio)

    args = parser.parse_args(argv)
    args.func(args)


if __name__== "__main__":
    main()

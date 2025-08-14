Instruções para instalação e utilização da nossa aplicação.

Enunciado

Construir uma aplicação em linha de comandos para registar despesas e receitas, definir orçamentos por categoria e gerar relatórios mensais/semanal, sinalizando desvios (overspend).

Funcionalidades-chave

- Registo de movimentos (despesa/receita) com: data ISO, valor, categoria, descrição, método de pagamento.

- Orçamentos por categoria e período (mensal por omissão).

- Relatórios: totais por categoria/período; top categorias; cashflow por semana; alerta de orçamento excedido.

- Importação opcional de CSV externo (bónus).


Arquitetura por classes

- models.py — TipoMovimento(Enum), Movimento, Orcamento.

- storage.py — classe Storage: leitura/escrita de movimentos.json, orcamentos.json, exportações.

- service.py — classe FinanceService: regras de negócio, cálculos e alertas.

- cli.py — subcomandos com argparse.

- reports.py — geração de relatórios e exportação CSV/JSON.

Persistência
- movimentos.json — lista de movimentos.

- orcamentos.json — lista de orçamentos.

- relatorios/ — ficheiros exportados.


Tabela de comandos (proposta)

| Comando   | Argumentos principais                                                     | Descrição                       |
|-----------|---------------------------------------------------------------------------|---------------------------------|
| add-mov   | --tipo, --data, --valor, --categoria, --descricao, --metodo               | Adiciona um movimento           |
| list-mov  | --inicio, --fim, --categoria, --tipo, --texto                             | Lista movimentos com filtros    |
| add-orc   | --categoria, --limite, --periodo                                          | Cria/atualiza orçamento         |
| list-orc  | --periodo                                                                 | Mostra orçamentos do período    |
| relatorio | --tipo, --inicio, --fim, --saida                                          | Gera relatório                  |
| rem-mov   | --id                                                                      | Remove um movimento             |



Entrega 1 — Bases do projeto (11/08/2025)

- Criar estrutura de diretórios e ficheiros base.

- Implementar classes TipoMovimento e Movimento com validação.

- Criar classe Storage para movimentos.json.

- Implementar subcomandos add-mov e list-mov (listar todos).

- Critério de aceitação: criar e listar pelo menos 3 movimentos.

- Entrega: código funcional + README com exemplos.


# Exemplo para adicionar movimento 1
python -m gestor.cli add-mov --data "2025-08-11T00:00:00" --tipo "despesa" --categoria "Alimentação" --descricao "Almoço no restaurante" --valor 50.0 --metodo "dinheiro"

# Exemplo para adicionar movimento 2
python -m gestor.cli add-mov --data "2025-08-11T15:54:00" --tipo "despesa" --categoria "Alimentaçao" --descricao "Almoço" --valor 50.0 --metodo "dinheiro"

# Exemplo para adicionar movimento 3
python -m gestor.cli add-mov --data "2025-08-11T15:55:00" --tipo "receita" --categoria "Salario" --descricao "Salário - Agosto" --valor 1050.0 --metodo "dinheiro"

# Exemplo para adicionar movimento 4
python -m gestor.cli add-mov --data "2025-08-11T15:56:00" --tipo "despesa" --categoria "Trasnporte" --descricao "Viagem de comboio" --valor 35.0 --metodo "cartão"

# Exemplo com valor negativo (lança exceção)
 python -m gestor.cli add-mov --tipo despesa --data 2025-08-11 --valor -2.00 --categoria Alimentação --descricao "Almoço no restaurante" --metodo dinheiro

# Exemplo para listar movimentos
python -m gestor.cli list-mov


Entrega 2 — Orçamentos e filtros (12/08/2025)

- Criar classe Orcamento e guardar em orcamentos.json.

- Implementar subcomandos add-orc e list-orc.

- Adicionar filtros a list-mov (por data, categoria, tipo, texto).

- Emitir aviso de overspend ao adicionar despesa.

- Critério de aceitação: orçamento mensal a funcionar com aviso em overspend.

- Entrega: código + mínimo de 3 testes unitários.

# Exemplo para adicionar orçamento
python -m gestor.cli add-orc --categoria "Alimentação" --limite 200

# Exemplo para emitir aviso de overspend ao adicionar despesa (lança excessão de ultrapassar o valor)
python -m gestor.cli add-mov --data "2025-08-12T12:00:00" --tipo "despesa" --categoria "Alimentação" --descricao "Jantar caro" --valor 250.0 --metodo "cartão"

# Exemplo de como filtrar por data
python -m gestor.cli list-mov --data "2025-08-11 15:56:00"

# Exemplo de como filtrar por categoria
python -m gestor.cli list-mov --categoria "Alimentação"

# Exemplo de como filtrar por tipo
python -m gestor.cli list-mov --tipo receita 

# Exemplo de como filtrar por descricao
python -m gestor.cli list-mov --descricao "Viagem de comboio"

# Exemplo para listar orçamentos
python -m gestor.cli list-orc
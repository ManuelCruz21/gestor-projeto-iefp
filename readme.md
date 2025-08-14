Instruções para instalação e utilização da nossa aplicação.

# Gestor de Despesas e Orçamentos – CLI

Aplicação em linha de comandos para registar despesas e receitas, definir orçamentos por categoria e gerar relatórios mensais/semanal, sinalizando desvios (overspend).

---

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


## Instalação

1. Clonar o repositório:

```bash
git clone https://github.com/ManuelCruz21/gestor-projeto-iefp
cd gestor-projeto-iefp
```
2. Instalar pytest:
```bash
pip install pytest
```

3. Verificar se está instalado:
```bash
pytest --version
```

Após estas recomendações, temos então as várias entregas e os requisitos pedidos:

*Entrega 1 — Bases do projeto (11/08/2025)*

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

# Pasta data com movimentos.json

*Entrega 2 — Orçamentos e filtros (12/08/2025)*

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

# Pasta data com movimentos.json e orçamentos.json

*Entrega 3 — Relatórios (13/08/2025)*
- Implementar reports.py com:

  - totais-por-cat

  - cashflow-semanal

  - top-categorias

  - alertas

- Adicionar exportação CSV/JSON.

- Critério de aceitação: gerar pelo menos 2 relatórios e ficheiros de saída.

- Entrega: código + exemplos em relatorios/.

# Exemplo de Relatório por categoria
python -m gestor.cli relatorio --categoria totais-por-cat

# Exemplo de Relatório por cashflow-semanal
python -m gestor.cli relatorio --categoria cashflow-semanal

# Exemplo de Relatório top-categorias
python -m gestor.cli relatorio --categoria top-categorias

# Exemplo de Relatório de alertas
python -m gestor.cli relatorio --categoria alertas

# Pasta data agora com os json anteriores e os relatórios em csv

*Entrega 4 — Qualidade final*
- Adicionar tratamento de exceções e logging.

- Completar documentação (README completo com instruções e limitações).

- Criar mínimo de 10 testes no total, cobertura ≥ 75% nos módulos de negócio.

- Marcar versão final com tag v1.0.

- Critério de aceitação: todos os testes a passar e execução via python -m finance.

- Entrega: código final + documentação completa.

No topo de cada ficheiro de testes no diretório tests tem escrito o comando ao qual se deve correr os testes

# Exemplo:
```bash
pytest -v tests/test_cli.py
```
4. Coverage:
Para correr a coverage temos de instalar primeiro 

```bash
pip install coverage
```

5. Verificar se está instalado 
```bash
coverage --version
```

6. Correr no terminal o seguinte comando para verificar a cobertura
```bash
pytest --cov=gestor --cov-report=term-missing -v
```

Fica então a seguinte estrutura de pastas:

gestor-projeto-iefp/
├─ gestor/
│ ├─ init.py
│ ├─ cli.py # Interface de linha de comandos
│ ├─ models.py # Classe Tarefa e validações
│ ├─ storage.py # Guardar/carregar dados em JSON e CSV
│ └─ service.py # Regras de negócio
├─ data/ # Ficheiros gerados pela aplicação (tarefas.json, sessoes.csv)
│ ├─ movimentos.json
│ ├─ orcamentos.json
│ ├─ relatorios_mov.csv
│ ├─ relatorios_orc.csv
├─ tests/ # Testes com pytest
│ ├─ init.py
│ ├─ test_cli.py
│ ├─ test_mov.py
│ ├─ test_orc.py
│ ├─ test_service.py
│ ├─ test_storage.py
└─ README.md

gestor-despesas/
├─ gestor/
│  ├─ __init__.py
│  ├─ cli.py
│  ├─ models.py
│  ├─ service.py
│  ├─ storage.py
│  ├─ reports.py
├─ tests/
│  ├─ test_cli.py
│  ├─ test_service.py
│  ├─ test_storage.py
├─ movimentos.json
├─ orcamentos.json
├─ README.md

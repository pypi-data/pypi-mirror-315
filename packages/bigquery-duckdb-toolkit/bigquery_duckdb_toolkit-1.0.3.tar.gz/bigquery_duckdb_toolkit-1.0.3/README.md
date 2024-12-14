# bigquery_duckdb_toolkit

`bigquery_duckdb_toolkit` é um pacote Python desenvolvido para facilitar o carregamento de dados do BigQuery e a execução de consultas SQL flexíveis no DuckDB. Ele permite carregar dados de qualquer tabela do BigQuery em um DataFrame pandas e realizar análises avançadas no DuckDB, sendo ideal para workflows de analytics engineering.

## Instalação

Para instalar a partir do PyPI, execute:

```bash
pip install bigquery_duckdb_toolkit
```

## Estrutura do Pacote

```plaintext
bigquery_duckdb_toolkit/
├── bigquery_duckdb_toolkit/
│   ├── __init__.py
│   ├── bigquery_client.py
│   ├── bigquery_to_pandas.py
│   └── interaction_service.py
├── setup.py
├── requirements.txt
└── README.md
```

### Módulos Principais

- **`BigQueryClient`**: Estabelece uma conexão com o BigQuery e executa consultas SQL.
- **`BigQueryToPandas`**: Carrega dados do BigQuery em um DataFrame pandas e aplica filtros e conversões de tipo.
- **`InteractionService`**: Carrega dados de qualquer tabela do BigQuery, registra-os no DuckDB e executa consultas SQL personalizadas.

## Exemplo de Uso

Neste exemplo, usaremos o conjunto de dados público `bigquery-public-data.samples.natality`, que contém dados de natalidade nos Estados Unidos. Vamos carregar dados para um DataFrame pandas, registrá-los no DuckDB e realizar uma consulta personalizada.

> Nota: Caso deseje filtrar por alguma chave primário ou estrangeira, utilizar o valor como string.

```python
from bigquery_duckdb_toolkit.interaction_service import InteractionService

# Configurações
project_id = 'bigquery-public-data'
table_name = 'bigquery-public-data.samples.natality'

# Inicialize o serviço de interação
interaction_service = InteractionService(project_id)

# Carregue os dados do BigQuery com um filtro flexível e registre-os no DuckDB
filters = {"year": "2000", "state": "CA"}  # Exemplo de filtro para registros de 2000 na Califórnia
df = interaction_service.load_data_to_duckdb(table_name, filters, duckdb_table_name='natality')

# Execute uma consulta personalizada no DuckDB
# Exemplo: Contar o número de nascimentos por mês na Califórnia em 2000
query = """
  SELECT month, COUNT(*) AS births_count
  FROM natality
  GROUP BY month
  ORDER BY births_count DESC
"""
result_df = interaction_service.run_duckdb_query(query)

# Exibir os resultados
interaction_service.display_query_results(query)
```

## API do Pacote

### `InteractionService`

- **`load_data_to_duckdb(table_name, filters=None, duckdb_table_name='temp_table')`**: 
  Carrega dados de uma tabela BigQuery em um DataFrame pandas com filtros opcionais e registra-o como uma tabela no DuckDB.

  - **Parâmetros**:
    - `table_name` (str): Nome da tabela BigQuery no formato `project.dataset.table`.
    - `filters` (dict, opcional): Dicionário com filtros para aplicar à consulta. Exemplo: `{"coluna": "valor"}`.
    - `duckdb_table_name` (str, opcional): Nome para registrar a tabela no DuckDB (padrão: `'temp_table'`).

  - **Retorno**: `pd.DataFrame` com os dados filtrados.

- **`run_duckdb_query(query)`**: Executa uma consulta SQL no DuckDB e retorna os resultados em um DataFrame pandas.

  - **Parâmetros**:
    - `query` (str): Consulta SQL a ser executada.

  - **Retorno**: `pd.DataFrame` com os resultados da consulta.

- **`display_query_results(query)`**: Executa uma consulta SQL no DuckDB e exibe os resultados, útil para visualização em notebooks.

  - **Parâmetros**:
    - `query` (str): Consulta SQL a ser executada.

## Contribuindo

Contribuições são bem-vindas! Abra issues e pull requests conforme necessário. Para contribuições maiores, entre em contato para discutir as mudanças propostas.

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

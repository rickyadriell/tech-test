# Fluent Software Engineering Tech Test Tools

### Setup

You will need to add a `.env` file with:

* `DEFAULT_DATASET` - the BigQuery dataset you want to run queries on
* `SERVICE_ACCOUNT_JSON` - the JSON key for the BigQuery service account that has permissions to run jobs

Install dependencies with poetry:

1. Run `poetry install`

## Usage

 `poetry run python main.py`,

## `query_bigquery` from `query_bigquery.py`

Use this function to run a SQL snippet on BigQuery

## `generate_sql` from `semantic_layer_engine.py`

This function builds SQL queries based on a given query and semantic layer.

### Classes

#### `SQLQueryBuilder`

A class to build SQL queries based on a given query and semantic layer.

**Methods:**

* `__init__(self, query: Query, semantic_layer: SemanticLayer)`: Initialize the SQLQueryBuilder with a query and semantic layer.
* `find_metric(self, name: str) -> Optional[Metric]`: Find a metric definition by name.
* `find_dimension(self, name: str) -> Optional[Dimension]`: Find a dimension definition by name.
* `build_select(self)`: Build the SELECT clause of the SQL query.
* `build_where(self)`: Build the WHERE and HAVING clause of the SQL query.
* `build_joins(self)`: Build the JOIN clauses of the SQL query.
* `build_sql(self) -> str`: Build the complete SQL query.

### Functions

#### `generate_sql(query: Query, semantic_layer: SemanticLayer) -> str`

Generate an SQL query based on a given query and semantic layer.

**Parameters:**

* `query`: The query definition containing metrics, dimensions, and filters.
* `semantic_layer`: The semantic layer definition containing metrics, dimensions, and joins.

**Returns:**

* The generated SQL query as a string.

**Raises:**

* `ValueError`: If there is an error generating the SQL query.

### Example Usage

```python
from semantic_layer_engine import Query, SemanticLayer, generate_sql

query: Query = {
    "metrics": [
        "order_count"
    ]
},

semantic_layer: SemanticLayer = {
    "metrics": [
        {
            "name": "order_count",
            "sql": "COUNT(*)",
            "table": "orders"
        }
    ]
},

sql = generate_sql(query, semantic_layer)
print(sql)
```

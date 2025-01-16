from typing import Dict, List, Union, TypedDict, Optional


class Filter(TypedDict):
    field: str
    operator: str
    value: Union[str, int, float]


class Query(TypedDict):
    metrics: List[str]
    dimensions: Optional[List[str]]
    filters: Optional[List[Filter]]


class Metric(TypedDict):
    name: str
    sql: str
    table: str


class Dimension(TypedDict):
    name: str
    sql: str
    table: str


class Join(TypedDict):
    one: str
    many: str
    join: str


class SemanticLayer(TypedDict):
    metrics: List[Metric]
    dimensions: Optional[List[Dimension]]
    joins: Optional[List[Join]]


class SQLQueryBuilder:
    """
    A class to build SQL queries based on a given query and semantic layer.
    """

    def __init__(self, query: Query, semantic_layer: SemanticLayer):
        """
        Initialize the SQLQueryBuilder with a query and semantic layer.

        :param query: The query definition containing metrics, dimensions, and filters.
        :param semantic_layer: The semantic layer definition containing metrics, dimensions, and joins.
        """
        self.query = query
        self.semantic_layer = semantic_layer
        self.select_clauses = []
        self.from_table = ""
        self.where_clauses = []
        self.group_by_clauses = []
        self.having_clauses = []
        self.join_clauses = []
        self.order_by_clauses = []

    def find_metric(self, name: str) -> Optional[Metric]:
        """
        Find a metric definition by name.

        :param name: The name of the metric to find.
        :return: The metric definition if found, otherwise None.
        """
        for metric in self.semantic_layer["metrics"]:
            if metric["name"] == name:
                return metric
        return None

    def find_dimension(self, name: str) -> Optional[Dimension]:
        """
        Find a dimension definition by name.

        :param name: The name of the dimension to find.
        :return: The dimension definition if found, otherwise None.
        """
        for dimension in self.semantic_layer["dimensions"]:
            if dimension["name"] == name or dimension["name"].startswith("ordered_date"):
                return dimension
        return None

    def build_select(self):
        """
        Build the SELECT clause of the SQL query.
        """
        for metric in self.query.get("metrics", []):
            metric_def = self.find_metric(metric)
            if metric_def is not None:
                self.select_clauses.append(f'{metric_def["sql"]} AS {metric}')
                self.from_table = metric_def["table"]

        for dimension in self.query.get("dimensions", []):
            dimension_def = self.find_dimension(dimension)
            if dimension_def is not None:
                if dimension.startswith("ordered_date__"):
                    period = dimension.split("__")[1]
                    self.select_clauses.append(
                        f'DATE_TRUNC({dimension_def["table"]}.{dimension_def["sql"]}, {period.upper()}) AS {dimension}')
                    self.group_by_clauses.append(f'{dimension}')
                    self.order_by_clauses.append(f'{dimension} ASC')
                else:
                    if len(self.semantic_layer.get("joins", [])) > 0:
                        self.select_clauses.append(
                            f'{dimension_def["table"]}.{dimension_def["sql"]}')
                        self.group_by_clauses.append(
                            f'{dimension_def["table"]}.{dimension_def["sql"]}')
                    else:
                        self.select_clauses.append(dimension_def["sql"])
                        self.group_by_clauses.append(dimension_def["sql"])

    def build_where(self):
        """
        Build the WHERE and HAVING clause of the SQL query.
        """
        for filter in self.query.get("filters", []):
            field = filter["field"]
            operator = filter["operator"]
            value = filter["value"]
            dimension_def = self.find_dimension(field)
            metric_def = self.find_metric(field)
            if dimension_def is not None:
                if len(self.semantic_layer.get("joins", [])) > 0:
                    table_field = f'{dimension_def["table"]}.{dimension_def["sql"]}'
                else:
                    table_field = dimension_def["sql"]
                if isinstance(value, (int, float)):
                    self.where_clauses.append(
                        f'{table_field} {operator} {value}')
                else:
                    self.where_clauses.append(
                        f'{table_field} {operator} \'{value}\'')
            elif metric_def is not None:
                metric_field = f'{metric_def["name"]}'
                if isinstance(value, (int, float)):
                    self.having_clauses.append(
                        f'{metric_field} {operator} {value}')
                else:
                    self.having_clauses.append(
                        f'{metric_field} {operator} \'{value}\'')

    def build_joins(self):
        """
        Build the JOIN clauses of the SQL query.
        """
        for join in self.semantic_layer.get("joins", []):
            self.join_clauses.append(f'JOIN {join["one"]} ON {join["join"]}')

    def build_sql(self) -> str:
        """
        Build the complete SQL query.

        :return: The generated SQL query as a string.
        """
        self.build_select()
        self.build_where()
        self.build_joins()

        sql = f'SELECT {", ".join(self.select_clauses)} FROM {self.from_table}'
        if self.join_clauses:
            sql += f' {" ".join(self.join_clauses)}'
        if self.where_clauses:
            sql += f' WHERE {" AND ".join(self.where_clauses)}'
        if self.group_by_clauses:
            sql += f' GROUP BY {", ".join(self.group_by_clauses)}'
        if self.having_clauses:
            sql += f' HAVING {" AND ".join(self.having_clauses)}'
        if self.order_by_clauses:
            sql += f' ORDER BY {", ".join(self.order_by_clauses)}'

        return sql


def generate_sql(query: Query, semantic_layer: SemanticLayer) -> str:
    """
    Generate an SQL query based on a given query and semantic layer.

    :param query: The query definition containing metrics, dimensions, and filters.
    :param semantic_layer: The semantic layer definition containing metrics, dimensions, and joins.
    :return: The generated SQL query as a string.
    :raises ValueError: If there is an error generating the SQL query.
    """
    try:
        builder = SQLQueryBuilder(query, semantic_layer)
        return builder.build_sql()
    except Exception as e:
        raise ValueError(f"Error generating SQL: {e}")

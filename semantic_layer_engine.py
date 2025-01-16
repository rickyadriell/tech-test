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


def generate_sql(query: Query, semantic_layer: SemanticLayer) -> str:
    return ""

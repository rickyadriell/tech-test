from typing import Dict, List
from semantic_layer_engine import Query, SemanticLayer, generate_sql
from query_bigquery import query_bigquery
import json


def load_test_data() -> Dict[str, List[Dict[Query, SemanticLayer]]]:
    with open("test_data.json", "r") as file:
        test_data = json.load(file)
    return test_data["test_data"]


def get_query_results_based_on_test_data():
    for index, text_data in enumerate(load_test_data()):
        sql = text_data['expected_result']
        print(f"\n query_bigquery {index + 1}: {text_data['query_text']}")
        query_bigquery(sql)


def test_generate_sql():
    for index, text_data in enumerate(load_test_data()):
        print(f"\nExecuting Test {index + 1}: {text_data['query_text']}")
        query = text_data['query']
        semantic_layer = text_data['semantic_layer']
        expected_result = text_data['expected_result']
        result = generate_sql(query, semantic_layer)
        if expected_result == result:
            print("✅ Test Passed")
            print(f"Actual  : {result}")
        else:
            print(f"❌ Test Failed")
            print(f"Expected: {expected_result}")
            print(f"Actual  : {result}")


def get_actual_query_results_based_on_test_data():
    for index, text_data in enumerate(load_test_data()):
        print(f"\nExecuting Test {index + 1}: {text_data['query_text']}")
        query = text_data['query']
        semantic_layer = text_data['semantic_layer']
        expected_result = text_data['expected_result']
        result = generate_sql(query, semantic_layer)
        query_bigquery(result)


# Example Usage
if __name__ == "__main__":
    test_generate_sql()
    # get_actual_query_results_based_on_test_data()
    # get_query_results_based_on_test_data()

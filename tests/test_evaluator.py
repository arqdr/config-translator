import pytest
from src.evaluator import Evaluator

def test_evaluator_simple():
    evaluator = Evaluator()
    
    # Простые вычисления
    assert evaluator.evaluate_expression("5 3 +") == 8
    assert evaluator.evaluate_expression("10 2 -") == 8
    assert evaluator.evaluate_expression("4 3 *") == 12
    assert evaluator.evaluate_expression("10 2 /") == 5

def test_evaluator_variables():
    evaluator = Evaluator()
    evaluator.set_variable('port', 8080)
    
    result = evaluator.evaluate_expression("port 1000 +")
    assert result == 9080
import pytest
from src.transformer import ConfigTransformer
from src.parser import AssignmentNode, ValueNode, BlockNode

def test_transformer_simple():
    transformer = ConfigTransformer()
    
    # Создаем тестовый AST
    nodes = [
        AssignmentNode('name', ValueNode('test')),
        AssignmentNode('port', ValueNode(8080))
    ]
    
    result = transformer.ast_to_dict(nodes)
    
    assert result['name'] == 'test'
    assert result['port'] == 8080

def test_transformer_block():
    transformer = ConfigTransformer()
    
    block = BlockNode('server', [
        AssignmentNode('host', ValueNode('localhost')),
        AssignmentNode('port', ValueNode(8080))
    ])
    
    result = transformer.ast_to_dict([block])
    
    assert 'server' in result
    assert result['server']['host'] == 'localhost'
    assert result['server']['port'] == 8080
import pytest
from src.lexer import Lexer
from src.parser import Parser

def test_parser_assignment():
    source = "name = [[test]];"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert len(ast) == 1
    assert ast[0].key == 'name'
    assert ast[0].value.value == 'test'

def test_parser_block():
    source = "config = @{ key = [[value]]; };"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    
    assert len(ast) == 1
    assert ast[0].key == 'config'
    assert len(ast[0].assignments) == 1
    assert ast[0].assignments[0].key == 'key'
import pytest
from src.lexer import Lexer

def test_lexer_basic():
    source = "name = [[test]];"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert len(tokens) == 3
    assert tokens[0].type == 'IDENTIFIER'
    assert tokens[0].value == 'name'
    assert tokens[1].type == 'EQUALS'
    assert tokens[2].type == 'STRING'
    assert tokens[2].value == 'test'

def test_lexer_block():
    source = "config = @{ key = [[value]]; };"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    assert len(tokens) == 7
    assert tokens[0].type == 'IDENTIFIER'
    assert tokens[1].type == 'EQUALS'
    assert tokens[2].type == 'LBRACE'

def test_lexer_comment():
    source = "% comment\nname = [[test]];"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    # Комментарий должен быть пропущен
    assert len(tokens) == 3
    assert tokens[0].value == 'name'
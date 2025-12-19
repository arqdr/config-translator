"""
Парсер для построения AST из токенов.
"""
from typing import List, Optional, Dict, Any
from .lexer import Token

class ASTNode:
    pass

class AssignmentNode(ASTNode):
    def __init__(self, key: str, value):
        self.key = key
        self.value = value
    
    def __repr__(self):
        return f"Assignment({self.key} = {self.value})"

class BlockNode(ASTNode):
    def __init__(self, key: str, assignments: List[AssignmentNode]):
        self.key = key
        self.assignments = assignments
    
    def __repr__(self):
        return f"Block({self.key}, {len(self.assignments)} assignments)"

class ValueNode(ASTNode):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Value({self.value})"

class ExpressionNode(ASTNode):
    def __init__(self, expression: str):
        self.expression = expression
    
    def __repr__(self):
        return f"Expression({self.expression})"

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
    
    def parse(self) -> List[ASTNode]:
        statements = []
        
        while not self.is_at_end():
            # Пропускаем пустые токены
            if self.current().type in ['NEWLINE', 'COMMENT']:
                self.advance()
                continue
            
            # Блок @{ ... }
            if self.check('IDENTIFIER') and self.peek_next() and self.peek_next().type == 'LBRACE':
                statements.append(self.parse_block())
            # Обычное присваивание
            elif self.check('IDENTIFIER') and self.peek_next() and self.peek_next().type == 'EQUALS':
                statements.append(self.parse_assignment())
            else:
                self.advance()
        
        return statements
    
    def parse_assignment(self) -> AssignmentNode:
        key = self.consume('IDENTIFIER').value
        self.consume('EQUALS')
        value = self.parse_value()
        self.consume('SEMICOLON')
        return AssignmentNode(key, value)
    
    def parse_block(self) -> BlockNode:
        key = self.consume('IDENTIFIER').value
        self.consume('LBRACE')
        
        assignments = []
        while not self.check('RBRACE') and not self.is_at_end():
            # Пропускаем комментарии и пустые строки
            if self.current().type in ['NEWLINE', 'COMMENT']:
                self.advance()
                continue
            
            if self.check('IDENTIFIER') and self.peek_next() and self.peek_next().type == 'EQUALS':
                assignments.append(self.parse_assignment())
            elif self.check('IDENTIFIER') and self.peek_next() and self.peek_next().type == 'LBRACE':
                assignments.append(self.parse_block())
            else:
                self.advance()
        
        self.consume('RBRACE')
        return BlockNode(key, assignments)
    
    def parse_value(self) -> ASTNode:
        token = self.current()
        
        if token.type == 'STRING':
            self.advance()
            return ValueNode(token.value)
        elif token.type == 'NUMBER':
            self.advance()
            # Пробуем преобразовать в int или float
            try:
                if '.' in token.value:
                    value = float(token.value)
                else:
                    value = int(token.value)
            except ValueError:
                value = token.value
            return ValueNode(value)
        elif token.type == 'BOOLEAN':
            self.advance()
            return ValueNode(token.value == 'true')
        elif token.type == 'EXPRESSION':
            self.advance()
            return ExpressionNode(token.value)
        else:
            # Если что-то пошло не так, возвращаем как есть
            self.advance()
            return ValueNode(token.value)
    
    def current(self) -> Token:
        if self.is_at_end():
            return Token('EOF', '', 0, 0)
        return self.tokens[self.position]
    
    def advance(self) -> Token:
        if not self.is_at_end():
            self.position += 1
        return self.previous()
    
    def previous(self) -> Token:
        return self.tokens[self.position - 1]
    
    def check(self, type: str) -> bool:
        if self.is_at_end():
            return False
        return self.current().type == type
    
    def consume(self, type: str) -> Token:
        if self.check(type):
            return self.advance()
        raise SyntaxError(f"Expected {type}, got {self.current().type}")
    
    def peek_next(self) -> Optional[Token]:
        if self.position + 1 < len(self.tokens):
            return self.tokens[self.position + 1]
        return None
    
    def is_at_end(self) -> bool:
        return self.position >= len(self.tokens)
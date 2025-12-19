"""
Лексер для разбора конфигурационного языка на токены.
"""
from typing import List, Tuple, Optional
import re

class Token:
    def __init__(self, type: str, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, line={self.line})"

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
    def tokenize(self) -> List[Token]:
        while self.position < len(self.source):
            char = self.source[self.position]
            
            # Пропускаем пробелы
            if char in ' \t':
                self.advance()
                continue
            
            # Пропускаем комментарии
            if char == '%':
                self.skip_comment()
                continue
            
            # Новая строка
            if char == '\n':
                self.line += 1
                self.column = 1
                self.advance()
                continue
            
            # Строки [[...]]
            if self.match('[['):
                self.read_string()
                continue
            
            # Выражения $...$
            if char == '$':
                self.read_expression()
                continue
            
            # Блоки @{
            if self.match('@{'):
                self.add_token('LBRACE', '@{')
                continue
            
            # Конец блока };
            if self.match('};'):
                self.add_token('RBRACE', '};')
                continue
            
            # Присваивание =
            if char == '=':
                self.add_token('EQUALS', '=')
                continue
            
            # Конец инструкции ;
            if char == ';':
                self.add_token('SEMICOLON', ';')
                continue
            
            # Числа
            if char.isdigit():
                self.read_number()
                continue
            
            # Идентификаторы (ключи)
            if char.isalpha() or char == '_':
                self.read_identifier()
                continue
            
            # Булевы значения
            if self.match('true') or self.match('false'):
                value = 'true' if self.source.startswith('true', self.position - 4) else 'false'
                self.add_token('BOOLEAN', value)
                continue
            
            self.advance()
        
        return self.tokens
    
    def advance(self, n=1):
        self.position += n
        self.column += n
    
    def match(self, pattern: str) -> bool:
        if self.source.startswith(pattern, self.position):
            self.advance(len(pattern))
            return True
        return False
    
    def skip_comment(self):
        while self.position < len(self.source) and self.source[self.position] != '\n':
            self.advance()
    
    def read_string(self):
        start = self.position
        start_line = self.line
        start_col = self.column
        
        # Пропускаем [[
        self.advance(2)
        
        # Читаем до ]]
        while self.position < len(self.source) - 1:
            if self.source[self.position:self.position+2] == ']]':
                value = self.source[start+2:self.position]
                self.advance(2)  # Пропускаем ]]
                self.add_token('STRING', value, start_line, start_col)
                return
            self.advance()
    
    def read_expression(self):
        start = self.position
        start_line = self.line
        start_col = self.column
        
        self.advance()  # Пропускаем $
        
        # Читаем до $
        while self.position < len(self.source):
            if self.source[self.position] == '$':
                value = self.source[start+1:self.position]
                self.advance()  # Пропускаем $
                self.add_token('EXPRESSION', value, start_line, start_col)
                return
            self.advance()
    
    def read_number(self):
        start = self.position
        start_line = self.line
        start_col = self.column
        
        while self.position < len(self.source) and (self.source[self.position].isdigit() or self.source[self.position] == '.'):
            self.advance()
        
        value = self.source[start:self.position]
        self.add_token('NUMBER', value, start_line, start_col)
    
    def read_identifier(self):
        start = self.position
        start_line = self.line
        start_col = self.column
        
        while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
            self.advance()
        
        value = self.source[start:self.position]
        self.add_token('IDENTIFIER', value, start_line, start_col)
    
    def add_token(self, token_type: str, value: str, line=None, column=None):
        if line is None:
            line = self.line
        if column is None:
            column = self.column
        self.tokens.append(Token(token_type, value, line, column))
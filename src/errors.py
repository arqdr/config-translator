"""
Ошибки для конфигурационного транслятора.
"""
class ConfigError(Exception):
    """Базовая ошибка конфигурации."""
    pass

class LexerError(ConfigError):
    """Ошибка лексического анализа."""
    def __init__(self, message, line, column):
        super().__init__(f"[Lexer] {message} (строка {line}, позиция {column})")
        self.line = line
        self.column = column

class ParserError(ConfigError):
    """Ошибка синтаксического анализа."""
    def __init__(self, message, line=None):
        if line:
            super().__init__(f"[Parser] {message} (строка {line})")
        else:
            super().__init__(f"[Parser] {message}")
        self.line = line

class EvaluatorError(ConfigError):
    """Ошибка вычисления выражения."""
    pass
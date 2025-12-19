"""
Вычислитель выражений $...$
"""
class Evaluator:
    def __init__(self):
        self.variables = {}
    
    def evaluate_expression(self, expression: str, context: dict = None) -> any:
        """
        Упрощенный evaluator для выражений вида $a b +$
        В реальном проекте нужно реализовать полноценный парсер выражений.
        """
        if context:
            self.variables.update(context)
        
        # Простая замена переменных
        for var_name, value in self.variables.items():
            expression = expression.replace(var_name, str(value))
        
        # Упрощенная обработка
        tokens = expression.split()
        
        # Если это просто число после замены
        if len(tokens) == 1:
            try:
                if '.' in tokens[0]:
                    return float(tokens[0])
                return int(tokens[0])
            except ValueError:
                return tokens[0]
        
        # Базовая поддержка простых операций
        stack = []
        for token in tokens:
            if token.isdigit() or (token.replace('.', '').isdigit() and token.count('.') == 1):
                if '.' in token:
                    stack.append(float(token))
                else:
                    stack.append(int(token))
            elif token == '+':
                b = stack.pop()
                a = stack.pop()
                stack.append(a + b)
            elif token == '-':
                b = stack.pop()
                a = stack.pop()
                stack.append(a - b)
            elif token == '*':
                b = stack.pop()
                a = stack.pop()
                stack.append(a * b)
            elif token == '/':
                b = stack.pop()
                a = stack.pop()
                if b != 0:
                    stack.append(a / b)
                else:
                    stack.append(0)
            else:
                # Пробуем получить значение переменной
                if token in self.variables:
                    stack.append(self.variables[token])
                else:
                    stack.append(token)
        
        return stack[0] if stack else 0
    
    def set_variable(self, name: str, value):
        self.variables[name] = value
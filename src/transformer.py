"""
Преобразователь AST в Python-словарь.
"""
import tomlkit
from typing import Dict, Any, List
from .parser import ASTNode, AssignmentNode, BlockNode, ValueNode, ExpressionNode
from .evaluator import Evaluator

class ConfigTransformer:
    def __init__(self):
        self.evaluator = Evaluator()
    
    def ast_to_dict(self, nodes: List[ASTNode]) -> Dict[str, Any]:
        result = {}
        
        for node in nodes:
            if isinstance(node, AssignmentNode):
                value = self.node_to_value(node.value)
                result[node.key] = value
                # Сохраняем для evaluator
                self.evaluator.set_variable(node.key, value)
            
            elif isinstance(node, BlockNode):
                block_dict = self.ast_to_dict(node.assignments)
                result[node.key] = block_dict
                # Для evaluator сохраняем как namespace
                self.evaluator.set_variable(node.key, block_dict)
        
        return result
    
    def node_to_value(self, node: ASTNode) -> Any:
        if isinstance(node, ValueNode):
            return node.value
        elif isinstance(node, ExpressionNode):
            # Пробуем вычислить выражение
            try:
                return self.evaluator.evaluate_expression(node.expression)
            except:
                # Если не получилось, возвращаем как строку
                return f"${{{node.expression}}}"  # Делаем более читаемым
        elif isinstance(node, BlockNode):
            return self.ast_to_dict(node.assignments)
        
        return str(node)
    
    def to_toml(self, config_dict: Dict[str, Any]) -> str:
        """Преобразует словарь в TOML строку."""
        doc = tomlkit.document()
        
        def add_to_doc(data, doc_part):
            for key, value in data.items():
                if isinstance(value, dict):
                    table = tomlkit.table()
                    add_to_doc(value, table)
                    doc_part[key] = table
                else:
                    doc_part[key] = value
        
        add_to_doc(config_dict, doc)
        return tomlkit.dumps(doc)
"""
Командный интерфейс для конфигурационного транслятора.
"""
import argparse
import sys
from pathlib import Path
from .lexer import Lexer
from .parser import Parser
from .transformer import ConfigTransformer

def main():
    parser = argparse.ArgumentParser(
        description='Конвертер учебного конфигурационного языка в TOML'
    )
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Входной файл .cfg'
    )
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Выходной файл .toml'
    )
    
    args = parser.parse_args()
    
    # Проверяем существование входного файла
    input_path = Path(args.input)
    if not input_path.exists():
        print(f'❌ Ошибка: Файл {args.input} не найден', file=sys.stderr)
        sys.exit(1)
    
    try:
        # Читаем входной файл
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Лексический анализ
        lexer = Lexer(content)
        tokens = lexer.tokenize()
        
        # Синтаксический анализ
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Преобразование в словарь и TOML
        transformer = ConfigTransformer()
        config_dict = transformer.ast_to_dict(ast)
        toml_content = transformer.to_toml(config_dict)
        
        # Записываем выходной файл
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(toml_content)
        
        print(f'✅ Конфигурация успешно преобразована в {args.output}')
        
    except Exception as e:
        print(f'❌ Ошибка преобразования: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
import pytest
import tempfile
import os
from src.cli import main
import sys
from io import StringIO

def test_integration_basic():
    # Создаем временные файлы
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cfg', delete=False) as cfg:
        cfg.write('name = [[test]];\nport = 8080;')
        cfg_path = cfg.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as toml:
        toml_path = toml.name
    
    try:
        # Мокаем sys.argv
        old_argv = sys.argv
        sys.argv = ['cli.py', '-i', cfg_path, '-o', toml_path]
        
        # Перехватываем вывод
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        # Запускаем
        main()
        
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        assert 'успешно преобразована' in output
        
        # Проверяем что файл создан
        assert os.path.exists(toml_path)
        
    finally:
        sys.argv = old_argv
        # Удаляем временные файлы
        os.unlink(cfg_path)
        if os.path.exists(toml_path):
            os.unlink(toml_path)
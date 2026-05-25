import pytest
from pathlib import Path
from backend.core.code_parser import CodeParser

def test_parse_python_file():
    parser = CodeParser()
    
    # Create test file
    test_code = """
def hello_world():
    '''A simple greeting function.'''
    print("Hello, World!")

class MyClass:
    def __init__(self):
        self.value = 42
"""
    
    test_file = Path("test_sample.py")
    test_file.write_text(test_code)
    
    entities = parser.parse_file(test_file)
    
    # Assertions
    assert len(entities) > 0
    function_names = [e.name for e in entities if e.type == 'function']
    assert 'hello_world' in function_names
    
    class_names = [e.name for e in entities if e.type == 'class']
    assert 'MyClass' in class_names
    
    # Cleanup
    test_file.unlink()

def test_dependency_extraction():
    parser = CodeParser()
    
    test_code = """
def process_data():
    result = calculate()
    return format_output(result)

def calculate():
    return 42

def format_output(data):
    return str(data)
"""
    
    test_file = Path("test_deps.py")
    test_file.write_text(test_code)
    
    entities = parser.parse_file(test_file)
    
    # Check dependencies
    process_data = [e for e in entities if e.name == 'process_data'][0]
    assert 'calculate' in process_data.dependencies
    assert 'format_output' in process_data.dependencies
    
    test_file.unlink()
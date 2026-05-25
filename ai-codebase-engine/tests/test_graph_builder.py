import pytest
from backend.core.graph_builder import GraphBuilder

def test_build_graph():
    entities = [
        {
            'name': 'main',
            'type': 'function',
            'file_path': 'main.py',
            'dependencies': ['helper']
        },
        {
            'name': 'helper',
            'type': 'function',
            'file_path': 'utils.py',
            'dependencies': []
        }
    ]
    
    builder = GraphBuilder()
    graph = builder.build_graph(entities)
    
    assert graph.number_of_nodes() == 2
    assert graph.number_of_edges() >= 0

def test_circular_dependency_detection():
    entities = [
        {
            'name': 'func_a',
            'type': 'function',
            'file_path': 'a.py',
            'dependencies': ['func_b']
        },
        {
            'name': 'func_b',
            'type': 'function',
            'file_path': 'b.py',
            'dependencies': ['func_a']
        }
    ]
    
    builder = GraphBuilder()
    graph = builder.build_graph(entities)
    cycles = builder.find_circular_dependencies()
    
    assert len(cycles) > 0
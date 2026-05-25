import networkx as nx
from typing import List, Dict, Optional

class GraphBuilder:
    """Build dependency graphs from code entities."""
    
    def __init__(self):
        self.graph = nx.DiGraph()
    
    def build_graph(self, entities: List[Dict]) -> nx.DiGraph:
        """Build dependency graph from parsed entities."""
        self.graph.clear()
        
        # Add nodes
        for entity in entities:
            node_id = f"{entity['file_path']}::{entity['name']}"
            self.graph.add_node(
                node_id,
                type=entity['type'],
                name=entity['name'],
                file=entity['file_path'],
                line=entity.get('line_start', 0)
            )
        
        # Add edges (dependencies)
        for entity in entities:
            source_id = f"{entity['file_path']}::{entity['name']}"
            
            if 'dependencies' in entity and entity['dependencies']:
                for dep in entity['dependencies']:
                    # Find matching entity
                    target_id = self._find_entity_id(entities, dep, entity['file_path'])
                    if target_id:
                        self.graph.add_edge(source_id, target_id, type='calls')
        
        return self.graph
    
    def get_function_dependencies(self, function_name: str) -> Dict:
        """Get all dependencies for a function."""
        matching_nodes = [
            node for node, data in self.graph.nodes(data=True)
            if data.get('name') == function_name and data.get('type') == 'function'
        ]
        
        if not matching_nodes:
            return {"error": "Function not found"}
        
        node = matching_nodes[0]
        
        return {
            "function": node,
            "direct_dependencies": list(self.graph.successors(node)),
            "dependent_on_this": list(self.graph.predecessors(node)),
            "all_dependencies": list(nx.descendants(self.graph, node))
        }
    
    def find_circular_dependencies(self) -> List[List[str]]:
        """Detect circular dependencies."""
        try:
            cycles = list(nx.simple_cycles(self.graph))
            return cycles
        except:
            return []
    
    def get_most_complex_functions(self, top_n: int = 10) -> List[Dict]:
        """Find functions with most dependencies."""
        complexity = []
        
        for node in self.graph.nodes():
            if self.graph.nodes[node].get('type') == 'function':
                out_degree = self.graph.out_degree(node)
                in_degree = self.graph.in_degree(node)
                
                complexity.append({
                    "function": self.graph.nodes[node]['name'],
                    "file": self.graph.nodes[node]['file'],
                    "dependencies": out_degree,
                    "used_by": in_degree,
                    "total_complexity": out_degree + in_degree
                })
        
        return sorted(complexity, key=lambda x: x['total_complexity'], 
                     reverse=True)[:top_n]
    
    def export_to_json(self) -> Dict:
        """Export graph to JSON for visualization."""
        nodes = []
        edges = []
        
        for node in self.graph.nodes():
            nodes.append({
                "id": node,
                **self.graph.nodes[node]
            })
        
        for edge in self.graph.edges():
            edges.append({
                "source": edge[0],
                "target": edge[1],
                **self.graph.edges[edge]
            })
        
        return {"nodes": nodes, "edges": edges}
    
    def _find_entity_id(self, entities: List[Dict], name: str, 
                       current_file: str) -> Optional[str]:
        """Find entity ID by name, prioritizing same file."""
        candidates = [
            entity for entity in entities
            if entity.get('name') == name and entity.get('type') != 'import'
        ]

        # First check same file.
        for entity in candidates:
            if entity.get('file_path') == current_file:
                return f"{entity['file_path']}::{entity['name']}"
        
        # Then check all files only when the symbol resolves unambiguously.
        if len(candidates) == 1:
            entity = candidates[0]
            return f"{entity['file_path']}::{entity['name']}"
        
        return None

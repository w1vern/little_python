from typing import Dict, Set, List, Any

class Graph:
    def __init__(self) -> None:
        self.nodes : Set[int] = set()
        self.edges : Dict[int, List[int]] = dict()
    
    def add_vertex(self, vertex : int) -> None:
        if vertex not in self.nodes:
            self.nodes.add(vertex)
            self.edges[vertex] = list()
    
    def add_edge(self, vertex_1 : int, vertex_2 : int, unidirectional : bool = False) -> None:
        if vertex_1 in self.nodes and vertex_2 in self.nodes:
            self.edges[vertex_1].append(vertex_2)
            if not unidirectional:
                self.edges[vertex_2].append(vertex_1)
            
    def get_vertices(self) -> Set[int]:
        return self.nodes
    
    def get_edges(self) -> Dict[int, List[int]]:
        return self.edges
    
    def __str__(self):
        return f"Vertices: {self.nodes}\nEdges: {self.edges}"
    
graph = Graph()

graph.add_vertex(1)
graph.add_vertex(3)
graph.add_vertex(2)
graph.add_vertex(4)
graph.add_vertex(5)

graph.add_edge(1, 2)
graph.add_edge(1, 3)
graph.add_edge(1, 5, True)
graph.add_edge(2, 3)
graph.add_edge(3, 4)
graph.add_edge(4, 5)
graph.add_edge(2, 4)
graph.add_edge(1, 4, True)

print(graph)
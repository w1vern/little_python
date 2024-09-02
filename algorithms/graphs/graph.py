from typing import Dict, Set, List, Any

import queue


class Graph:
    def __init__(self) -> None:
        self.nodes: Set[int] = set()
        self.edges: Dict[int, List[int]] = dict()

    def add_node(self, node: int) -> None:
        if node not in self.nodes:
            self.nodes.add(node)
            self.edges[node] = list()

    def add_edge(self, node_1: int, node_2: int, unidirectional: bool = False) -> None:
        if node_1 in self.nodes and node_2 in self.nodes:
            self.edges[node_1].append(node_2)
            if not unidirectional:
                self.edges[node_2].append(node_1)

    def get_nodes(self) -> Set[int]:
        return self.nodes

    def get_edges(self) -> Dict[int, List[int]]:
        return self.edges

    def breadth_first_search(self, node_to_find: int, start_node: int) -> int:
        if node_to_find not in self.nodes or start_node not in self.nodes:
            return -1
        queue_of_nodes = queue.Queue()
        set_of_checked = set()
        queue_of_nodes.put((start_node, 0))
        while not queue_of_nodes.empty():
            cur_node, path = queue_of_nodes.get()
            if cur_node in set_of_checked:
                continue
            if cur_node == node_to_find:
                return path
            set_of_checked.add(cur_node)
            for node in self.edges[cur_node]:
                if not node in set_of_checked:
                    queue_of_nodes.put((node, path + 1))
        return -1

    def depth_first_search(self, node_to_find: int, start_node: int) -> List[int]:
        if node_to_find not in self.nodes or start_node not in self.nodes:
            return []
        
        def dfs(current_node: int, path: List[int]) -> List[int]:
            if current_node == node_to_find:
                return path + [current_node]
            if current_node in set_of_checked:
                return []
            
            set_of_checked.add(current_node)
            for node in self.edges[current_node]:
                if node not in set_of_checked:
                    result_path = dfs(node, path + [current_node])
                    if result_path:
                        return result_path
            return []

        set_of_checked = set()
        return dfs(start_node, [])

    def __str__(self):
        return f"Nodes: {self.nodes}\nEdges: {self.edges}"


graph = Graph()

graph.add_node(1)
graph.add_node(3)
graph.add_node(2)
graph.add_node(4)
graph.add_node(5)

graph.add_edge(1, 2)
graph.add_edge(1, 3)
graph.add_edge(1, 5, True)
graph.add_edge(2, 3)
graph.add_edge(3, 4)
graph.add_edge(4, 5)
graph.add_edge(2, 4)
graph.add_edge(1, 4, True)

print(graph.depth_first_search(3, 1))

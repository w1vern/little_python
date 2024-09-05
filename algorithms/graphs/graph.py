import queue


class Graph:
    def __init__(self) -> None:
        self.nodes: set[str] = set()
        self.edges: dict[str, list[tuple[str, int]]] = dict()

    def add_node(self, node: str) -> None:
        if node not in self.nodes:
            self.nodes.add(node)
            self.edges[node] = list()

    def add_edge(self, node_1: str, node_2: str, weight: int = 1, unidirectional: bool = False) -> None:
        if node_1 in self.nodes and node_2 in self.nodes:
            self.edges[node_1].append((node_2, weight))
            if not unidirectional:
                self.edges[node_2].append((node_1, weight))

    def get_nodes(self) -> set[str]:
        return self.nodes

    def get_edges(self) -> dict[str, list[tuple[str, int]]]:
        return self.edges

    def breadth_first_search(self, node_to_find: str, start_node: str) -> int:
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
            for node in list(map(lambda x: x[0], self.edges[cur_node])):
                if not node in set_of_checked:
                    queue_of_nodes.put((node, path + 1))
        return -1

    def depth_first_search(self, node_to_find: str, start_node: str) -> list[str]:
        if node_to_find not in self.nodes or start_node not in self.nodes:
            return []
        
        def dfs(current_node: str, path: list[str]) -> list[str]:
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

    def Dijkstra(self, node_to_find : str, start_node : str):
        pass

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

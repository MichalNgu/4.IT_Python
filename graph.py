class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.is_weighted = False
        self.nodes = {}

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = {}

    def add_edge(self, u, v, weight=None):
        self.add_node(u)
        self.add_node(v)

        if weight is not None:
            self.is_weighted = True

        self.nodes[u][v] = weight

        if not self.directed and u != v:
            self.nodes[v][u] = weight

    def _get_edges_count(self):
        count = sum(len(neighbors) for neighbors in self.nodes.values())
        if not self.directed:
            loops = self._has_loops(count_only=True)
            return (count - loops) // 2 + loops
        return count

    def _has_loops(self, count_only=False):
        loops = 0
        for node, neighbors in self.nodes.items():
            if node in neighbors:
                if not count_only:
                    return True
                loops += 1
        return loops if count_only else False

    def _is_planar_heuristic(self):
        V = len(self.nodes)
        E = self._get_edges_count()
        
        if V < 3:
            return True
        if E > 3 * V - 6:
            return False
        return True

    def _greedy_coloring(self):
        sorted_nodes = sorted(self.nodes.keys(), key=lambda n: len(self.nodes[n]), reverse=True)
        result = {}
        
        for node in sorted_nodes:
            neighbor_colors = set()
            for neighbor in self.nodes[node]:
                if neighbor in result:
                    neighbor_colors.add(result[neighbor])
            
            color = 0
            while color in neighbor_colors:
                color += 1
            result[node] = color
            
        if not result:
            return 0
        return max(result.values()) + 1

    def print_graph(self):
        print("=== Struktura grafu ===")
        for node, neighbors in self.nodes.items():
            if not neighbors:
                print(f"{node} -> [žádné hrany]")
            else:
                edges_str = []
                for neighbor, weight in neighbors.items():
                    if weight is not None:
                        edges_str.append(f"{neighbor} (váha: {weight})")
                    else:
                        edges_str.append(f"{neighbor}")
                print(f"{node} -> {', '.join(edges_str)}")
        print("=======================\n")

    def analyze(self):
        print("=== Analýza grafu ===")
        V = len(self.nodes)
        E = self._get_edges_count()
        print(f"Počet uzlů (V): {V}")
        print(f"Počet hran (E): {E}")
        print(f"Orientovaný: {'Ano' if self.directed else 'Ne'}")
        print(f"Ohodnocený: {'Ano' if self.is_weighted else 'Ne'}")
        print(f"Obsahuje smyčky: {'Ano' if self._has_loops() else 'Ne'}")

        is_planar = self._is_planar_heuristic()
        if not is_planar:
            print("Planární: Ne")
        else:
            print("Planární: Pravděpodobně Ano")

        chromatic_num = self._greedy_coloring()
        print(f"Chromatické číslo (Greedy odhad): {chromatic_num}")
        print("==============================================\n")


if __name__ == "__main__":
    g = Graph(directed=False)
    
    g.add_edge("A", "B", weight=5)
    g.add_edge("B", "C", weight=2)
    g.add_edge("C", "A", weight=3)
    g.add_edge("C", "D")
    g.add_edge("D", "D")
    g.add_node("E")
    
    g.print_graph()
    g.analyze()
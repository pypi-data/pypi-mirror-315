# the vertex and graph classes for the rec engine. BFS is built in
from collections import deque

class Vertex:
    def __init__(self, value, rating=None):
        self.value = value
        self.rating = rating
        self.edges = {}

    def add_edge(self, vertex, weight=0):
        self.edges[vertex] = weight

class Graph:
    def __init__(self, directed=False):
        self.graph_dict = {}
        self.directed = directed

    def add_vertex(self, vertex):
        self.graph_dict[vertex.value] = vertex

    def add_edge(self, from_vertex, to_vertex, weight=0):
        self.graph_dict[from_vertex.value].add_edge(to_vertex.value, weight)
        if not self.directed:
            self.graph_dict[to_vertex.value].add_edge(from_vertex.value, weight)

    def get_vertex(self, value):
        return self.graph_dict.get(value)

    def bfs(self, start_vertex_name):
        if start_vertex_name not in self.graph_dict:
            return []
        visited = set()
        queue = deque([self.graph_dict[start_vertex_name]])
        result = []

        while queue:
            current_vertex = queue.popleft()
            if current_vertex.value not in visited:
                visited.add(current_vertex.value)
                result.append(current_vertex)
                for neighbor in current_vertex.edges:
                    if neighbor not in visited:
                        queue.append(self.graph_dict[neighbor])
        return result

# example usage 
# graph = Graph()
# create vertices
# action = Vertex("Action")
# game_a = Vertex("Game A", 4.5)
# game_b = Vertex("Game B", 4.7)
# add vertices to graph
# graph.add_vertex(action)
# graph.add_vertex(game_a)
# graph.add_vertex(game_b)
# add edges
# graph.add_edge(action, game_a)
# graph.add_edge(action, game_b)
# perform BFS
# games_in_action = graph.bfs("Action")
# for game in games_in_action:
# print(game.value, game.rating)

class Graph:
    vertices = []
    edges = []
    config = {}
    outdegree = {}

    def __init__(self, config):
        self.config = config
        self.vertices = list(config["jobs"].keys())
        for key, value in config["dependencies"].items():
            for val in value:
                self.edges.append( (key, val) )
        for v in self.vertices:
            self.outdegree[v] = 0
        for e in self.edges:
            self.outdegree[e[0]] = self.outdegree[e[0]]+1

    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        return self.edges

    def get_zero_outdegree_vertices(self):
        return []

    def remove_edge(self, edge):
        return

    def remove_vertex(self, edge):
        return


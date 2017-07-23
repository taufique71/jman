class Graph:
    def __init__(self, config):
        self.config = config
        self.vertices = list(config["jobs"].keys())
        self.edges = []
        for key, value in config["dependencies"].items():
            for val in value:
                self.edges.append( (key, val) )
        self.update_outdegree()
        return

    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        return self.edges

    def get_zero_outdegree_vertices(self):
        zero_outdegree_vertices = []
        for v in self.vertices:
            if self.outdegree[v] == 0:
                zero_outdegree_vertices.append(v)
        return zero_outdegree_vertices

    def update_outdegree(self):
        self.outdegree = {}
        for v in self.vertices:
            self.outdegree[v] = 0
        for e in self.edges:
            self.outdegree[e[0]] = self.outdegree[e[0]]+1
        return

    def remove_edge(self, edge):
        self.edges.remove( edge )
        self.update_outdegree()
        return

    def remove_vertex(self, vertex):
        self.vertices.remove(vertex)
        for e in list(self.edges):
            if e[1] == vertex:
                self.remove_edge(e)
        self.update_outdegree()
        return

class Graph:
    vertices = []
    edges = []
    config = {}
    outdegree = {}

    def update_outdegree(self):
        for v in self.vertices:
            self.outdegree[v] = 0
        for e in self.edges:
            self.outdegree[e[0]] = self.outdegree[e[0]]+1

    def __init__(self, config):
        self.config = config
        self.vertices = list(config["jobs"].keys())
        for key, value in config["dependencies"].items():
            for val in value:
                self.edges.append( (key, val) )
        self.update_outdegree()

    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        return self.edges

    def get_zero_outdegree_vertices(self):
        zero_outdegree_vertices = []
        for key, value in self.outdegree.items():
            if value == 0:
                zero_outdegree_vertices.append(key)
        return zero_outdegree_vertices

    def remove_edge(self, edge):
        try:
            self.edges.remove( edge )
            self.update_outdegree()
            return
        except:
            return

    def remove_vertex(self, vertex):
        try:
            self.vertices.remove(vertex)
            for e in self.edges:
                if e[0] == vertex or e[1] == vertex:
                    self.remove_edge(e)
            return
        except:
            return


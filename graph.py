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
        print(self.outdegree)
        zero_outdegree_vertices = []
        for v in self.vertices:
            if self.outdegree[v] == 0:
                zero_outdegree_vertices.append(v)
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
            # print("Before", self.edges)
            self.vertices.remove(vertex)
            for e in self.edges:
                # print("Checking out edge", e)
                # print(e[0], e[1], vertex)
                if e[0] == vertex or e[1] == vertex:
                    # print("Removing", edge)
                    self.remove_edge(e)
            # print("After", self.edges)
            return
        except:
            return


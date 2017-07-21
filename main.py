import json
import graph

def main():
    config = json.loads( open("config.json").read() )
    job_dependency_graph = graph.Graph(config)
    print(job_dependency_graph.get_vertices());
    print(job_dependency_graph.get_edges());

if __name__ == "__main__":
    main()

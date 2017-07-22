import json
import graph
import jobmanager

def main():
    config = json.loads( open("config.json").read() )
    job_dependency_graph = graph.Graph(config)
    out_file=open("./test_scripts/out.txt", "w")
    manager = jobmanager.Manager(job_dependency_graph, config, stdin=None, stdout=out_file, stderr=None)
    manager.start_jobs()
    # print(job_dependency_graph.outdegree);

if __name__ == "__main__":
    main()

import job
import graph
from threading import Lock

class Manager:
    def __init__(self, config, stdin=None, stdout=None, stderr=None):
        self.config = config
        self.stdout = stdout
        self.job_dependency_graph = graph.Graph(self.config)
        self.job_threads = {}
        self.job_status = {}
        self.lock = Lock()
        self.initialize_job_threads();

    def start_processing(self):
        zero_outdegree_vertices = self.job_dependency_graph.get_zero_outdegree_vertices()
        for v in zero_outdegree_vertices:
            self.job_status[v] = "processing"
            self.job_threads[v].start()

    def stop_processing(self):
        for key, val in self.job_threads.items():
            if self.job_threads[key].is_alive():
                self.job_threads[key].stop()
                self.job_threads[key].join()

    def initialize_job_threads(self):
        for key, val in self.config["jobs"].items():
            self.job_threads[key] = job.Job(key, val, parent=self, stdout=self.stdout)
            self.job_status[key] = "unprocessed"

    def get_job_status(self):
        return self.job_status

    def notify(self, job_key, job_status):
        print(job_key, job_status) 

    def on_job_finish(self, job_key, job_status):
        self.lock.acquire()
        if job_status == "success":
            self.notify(job_key, job_status)
            self.job_status[job_key] = "success"
            self.job_dependency_graph.remove_vertex(job_key)
            zero_outdegree_vertices = self.job_dependency_graph.get_zero_outdegree_vertices()
            for v in zero_outdegree_vertices:
                if self.job_status[v] == "unprocessed": 
                    self.job_status[v] = "processing"
                    self.job_threads[v].start()
        elif job_status == "failed":
            self.notify(job_key, job_status)
            self.job_status[job_key] = "failed"
        self.lock.release()

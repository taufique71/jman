import job

class Manager:
    def __init__(self, job_dependency_graph, job_config, stdin=None, stdout=None, stderr=None):
        self.job_dependency_graph = job_dependency_graph
        self.job_config = job_config
        self.all_jobs = {}
        self.job_status = {}
        for key, val in self.job_config["jobs"].items():
            self.all_jobs[key] = job.Job(key, val, parent=self, stdout=stdout)
            self.job_status[key] = None
        return

    def start_jobs(self):
        zero_outdegree_vertices = self.job_dependency_graph.get_zero_outdegree_vertices()
        for v in zero_outdegree_vertices:
            self.all_jobs[v].start()
        return

    def restart_job(self):
        # Logic to restart a previously failed job
        return

    def notify(self, job_key, job_status):
        print(job_key, job_status) 
        return

    def on_job_finish(self, job_key, job_status):
        if job_status == "success":
            self.notify(job_key, job_status)
            self.job_dependency_graph.remove_vertex(job_key)
            zero_outdegree_vertices = self.job_dependency_graph.get_zero_outdegree_vertices()
            for v in zero_outdegree_vertices:
                print(v)
                self.all_jobs[v].start()
        elif job_status == "failed":
            self.notify(job_key, job_status)


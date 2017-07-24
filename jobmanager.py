import job
import graph
from threading import Lock
import joblogmonitor

class Manager:
    def __init__(self, config, stdin=None, stdout=None, stderr=None):
        self.config = config
        self.stdout = stdout
        self.job_dependency_graph = None
        self.job_log_monitor = joblogmonitor.JobLogMonitor(self.config, parent=self)
        self.job_threads = {}
        self.job_status = {}
        self.lock = Lock()
        self.initialize_manager()
        self.job_log_monitor_start()

    def initialize_manager(self):
        print("[manager] > Initializing jobs")
        self.job_dependency_graph = graph.Graph(self.config)
        for key, val in self.config["jobs"].items():
            self.job_threads[key] = job.Job(key, val, parent=self, stdout=self.stdout)
            self.job_status[key] = "stopped"

    def job_log_monitor_start(self):
        print("[manager] > Stating database log monitor thread")
        self.job_log_monitor.start()

    def job_log_monitor_stop(self):
        print("[manager] > Stoping database log monitor thread")
        self.job_log_monitor.stop()
        self.job_log_monitor.join()

    def start(self, job_key=None):
        if job_key:
            if self.job_status[job_key]:
                if self.job_status[job_key] == "queued":
                    print("[manager] > You can't start a queued job without stopping it")
                elif self.job_status[job_key] == "processing":
                    print("[manager] > You can't start a job under processing without stopping it")
                elif self.job_status[job_key] == "success":
                    print("[manager] > You can't start a successfully processed job without restarting")
                else:
                    print("[manager] > Starting job ", job_key)
                    outdegree = self.job_dependency_graph.get_outdegree()
                    if outdegree[job_key] == 0:
                        self.job_status[job_key] = "processing"
                        self.job_threads[job_key].start()
                    else:
                        self.job_status[job_key] = "queued"

            else:
                print("[manager] > No such job")
        else:
            zero_outdegree_vertices = self.job_dependency_graph.get_zero_outdegree_vertices()
            vertices = self.job_dependency_graph.get_vertices()
            outdegree = self.job_dependency_graph.get_outdegree()
            flag = True
            for v in vertices:
                if self.job_status[v] == "queued" or self.job_status[v] == "processing":
                    flag = False
                    break
            if flag:
                print("[manager] > Starting job processing threads")
                for v in vertices:
                    if self.job_status[v] == "failed" or self.job_status[v] == "stopped":
                        if outdegree[v] == 0:
                            self.job_status[v] = "processing"
                            self.job_threads[v].start()
                        else:
                            self.job_status[v] = "queued"
            else:
                print("[manager] > You can't start already running or queued jobs without stopping them")

    def stop(self, job_key=None):
        if job_key:
            if self.job_status[job_key]:
                if self.job_status[job_key] == "stopped":
                    print("[manager] > You can't stop an already stopped job without starting it")
                elif self.job_status[job_key] == "failed":
                    print("[manager] > You can't stop a failed job without starting it")
                elif self.job_status[job_key] == "success":
                    print("[manager] > You can't stop a successfully processed job")
                elif self.job_status[job_key] == "queued":
                    print("[manager] > Stopping job ", job_key)
                    self.job_status[job_key] = "stopped"
                else:
                    print("[manager] > Stopping job ", job_key)
                    self.job_threads[job_key].stop()
                    self.job_threads[job_key].join()
                    self.job_threads[job_key] = job.Job(job_key, self.config["jobs"][job_key], parent=self, stdout=self.stdout)
                    self.job_status[job_key] = "stopped"
            else:
                print("[manager] > No such job")
        else:
            flag = True
            vertices = self.job_dependency_graph.get_vertices()
            for v in vertices:
                if self.job_status[v] == "stopped":
                    flag = False
            if flag:
                print("[manager] > Stopping job processing threads")
                for v in vertices:
                    if self.job_status[v] == "processing":
                        self.job_threads[v].stop()
                        self.job_threads[v].join()
                        self.job_threads[v] = job.Job(v, self.config["jobs"][v], parent=self, stdout=self.stdout)
                        self.job_status[v] = "stopped"
                    elif self.job_status[v] == "queued":
                        self.job_status[v] = "stopped"
            else:
                print("[manager] > You can't stop already stopped jobs without starting them")

    def restart(self):
        self.stop()
        self.initialize_manager()
        self.start()

    def status(self):
        return self.job_status

    def exit(self):
        self.stop()
        self.job_log_monitor_stop()

    def notify(self, message):
        print("[manager] >", message) 

    def on_job_finish(self, job_key, job_status):
        self.lock.acquire()
        if job_status == "success":
            self.notify(job_key +" >> " + job_status)
            self.job_status[job_key] = "success"
            self.job_dependency_graph.remove_vertex(job_key)
            zero_outdegree_vertices = self.job_dependency_graph.get_zero_outdegree_vertices()
            for v in zero_outdegree_vertices:
                if self.job_status[v] == "queued": 
                    self.job_status[v] = "processing"
                    self.job_threads[v].start()
        elif job_status == "failed":
            self.notify(job_key +" >> " + job_status)
            self.job_status[job_key] = "failed"
        self.lock.release()

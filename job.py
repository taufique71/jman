from threading import Thread
import subprocess

class Job(Thread):
    def __init__(self, job_key, job_details, parent=None, stdout=None):
        self.job_key = job_key
        self.job_details = job_details
        self.parent = parent
        self.stdout = stdout
        # if self.stdout == None:
            # self.stdout = open(self.job_details["path"] + job_key + ".txt", "w")
        super(Job, self).__init__()
        return

    def monitor(self, proc):
        outs, errs = proc.communicate()
        if errs:
            return "failed"
        else:
            return "success"
        return

    def run(self):
        script_to_run = self.job_details["path"] + self.job_details["script"]
        proc = subprocess.Popen(script_to_run, shell=True, stdout=self.stdout)
        job_status = self.monitor(proc)
        self.parent and self.parent.on_job_finish(self.job_key, job_status)

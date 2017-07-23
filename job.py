import threading
import subprocess
import psutil
import datetime
import time
import signal

class Job(threading.Thread):
    def __init__(self, job_key, job_details, parent, stdout=None):
        self.job_key = job_key
        self.job_details = job_details
        self.parent = parent
        self.stdout = stdout
        self.stop_event = threading.Event()
        super(Job, self).__init__()

    def stop(self):
        self.stop_event.set()

    def monitor(self, proc):
        parent = psutil.Process(proc.pid)
        parent_status = parent.status()
        children = parent.children(recursive=True)
        if parent_status != psutil.STATUS_ZOMBIE:
            if parent_status != psutil.STATUS_DEAD:
                return "processing"
            else:
                return "failed"
        else:
            if len(children) == 0:
                outs, errs = proc.communicate()
                if errs:
                    return "failed"
                else:
                    return "success"
            else:
                for c in children:
                    if c.status() == psutil.STATUS_DEAD:
                        return "failed"
                return "processing"

    def kill_processes(self, proc=None):
        if proc == None:
            return
        else:
            parent = psutil.Process(proc.pid)
            children = parent.children(recursive=True)
            for c in children:
                c.send_signal(signam.SIGTERM)
            parent.send_signal(signal.SIGTERM)

    def run(self):
        job_status = "processing"
        proc = None

        if self.job_details["time"]:
            today = datetime.date.today()
            target_time = datetime.datetime.strptime(self.job_details["time"], "%H:%M").time()
            target_datetime = datetime.datetime.combine(today, target_time)
            now = datetime.datetime.now()
            while now < target_datetime and self.stop_event.is_set() == False:
                time.sleep(1)
                now = datetime.datetime.now()

        if self.stop_event.is_set() == False:
            script_to_run = self.job_details["path"] + self.job_details["script"]
            proc = subprocess.Popen(script_to_run, shell=True, stdout=self.stdout)

        while self.stop_event.is_set() == False:
            job_status = self.monitor(proc)
            if job_status != "processing":
                break

        if self.stop_event.is_set() == False:
            self.parent.on_job_finish(self.job_key, job_status)
        else:
            self.kill_processes(proc)

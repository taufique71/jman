import threading
import datetime
import time
import pymysql

class JobLogMonitor(threading.Thread):
    def __init__(self, config, parent):
        self.config = config
        self.db_config = config["db_config"]
        self.connection = pymysql.connect(host=self.db_config["host"], user=self.db_config["user"], password=self.db_config["password"], db=self.db_config["db"], charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, autocommit=True)
        self.cursor = self.connection.cursor()
        self.parent = parent
        self.stop_event = threading.Event()
        super(JobLogMonitor, self).__init__()

    def stop(self):
        self.stop_event.set()

    def run(self):
        query_time = datetime.datetime.now()
        while self.stop_event.is_set() == False:
            query = "SELECT * FROM `job_log` WHERE `timestamp` > \"" + query_time.strftime('%Y-%m-%d %H:%M:%S') + "\""
            self.cursor.execute(query)
            self.connection.commit()
            query_time = datetime.datetime.now()
            for response in self.cursor:
                for k, v in self.config["jobs"].items():
                    if response["job_key"] == k:
                        if response["exec_time"] > v["expected_exec_time"]:
                            if response["amount_of_data"] > v["expected_amount_of_data"]:
                                message = response["job_key"] + " generated " + str(response["amount_of_data"]) + " data"
                                message = message + " in "
                                message = message + str(response["exec_time"]) + "s"
                                self.parent.notify(message)
                            if response["amount_of_data"] <= v["expected_amount_of_data"]:
                                message = response["job_key"] + " took " + str(response["exec_time"]) + "s"
                                self.parent.notify(message)
                        elif response["exec_time"] <= v["expected_exec_time"]:
                            if response["amount_of_data"] > v["expected_amount_of_data"]:
                                message = response["job_key"] + " generated " + str(response["amount_of_data"]) + " data"
                                self.parent.notify(message)
                            if response["amount_of_data"] <= v["expected_amount_of_data"]:
                                pass
            time.sleep(self.db_config["poll_interval"])

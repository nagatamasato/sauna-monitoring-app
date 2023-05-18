from datetime import datetime
import json
import os
import pymsteams
import collections
import re


class Witness:

    def __init__(self):
        # Teams Webhook
        self.__TEAMS_URL = "https://x1studiocojp.webhook.office.com/webhookb2/2359c523-6ff7-4e43-9cce-b924c34b9a1b@3e594155-a0af-40ef-a8f2-dc8ce23f3844/IncomingWebhook/5798f01fbb53408ea38a9651139d18ea/4eb77287-1789-4810-b206-e1c3bd304107"
        self.__teams_title = "TEST on Development Environment"
        self.__teams_text = ""
        self.__HOSTS_FILES = [
            "..\\hosts_1.json",
            "..\\hosts_2.json",
            "..\\hosts_3.json"
        ]
        self.__timeout_threshold = 1
        self.__monitor_witness_threshold = 10
        self.__alert_witness_threshold = 5
        self.__log_rotator_witness_threshold = 70
        self.__notes = '''<br>- - - - - - - - - - - - - - - - - - - - notes - - - - - - - - - - - - - - - - - - - -<br>
        [Connection]: Check if a timeout has occurred. Timeout threshold is {} sec.<br>
        [Health check]: Verify that the script is working properly by checking if the log update date/time is updated within the threshold.<br>
        The thresholds are as follows<br>
        ・monitor_[1-3]: {} sec<br>
        ・alert: {} sec<br>
        ・log_rotator: {} min<br>
        '''.format(self.__timeout_threshold, self.__monitor_witness_threshold, self.__alert_witness_threshold, self.__log_rotator_witness_threshold)

        #health check
        self.__health_check_message = ""
        self.__monitor_log_dir = "..\\monitor\\logs"
        self.__alert_log_dir = "..\\alert\\logs"
        self.__monitor_1_log_file_path = self.get_log_file_path('monitor_1')
        self.__monitor_2_log_file_path = self.get_log_file_path('monitor_2')
        self.__monitor_3_log_file_path = self.get_log_file_path('monitor_3')
        self.__alert_log_file_path = self.get_log_file_path('alert')

        # log rotation - monitor
        self.__monitor_log_rotation_log = "..\\log_rotator\\logs\\monitor-log_rotator-log.csv"
        self.__monitor_log_rotation_message = ""

        # log rotation - alert
        self.__alert_log_rotation_log = "..\\log_rotator\\logs\\alert-log_rotator-log.csv"
        self.__alert_log_rotation_message = ""

        # connection
        self.__sauna_connection_message = ""
        self.__chime_connection_message = ""

    def report(self):
        teams_message = pymsteams.connectorcard(self.__TEAMS_URL)
        teams_message.title(self.__teams_title)
        self.get_teams_text()
        teams_message.text(self.__teams_text)
        teams_message.send()


    def get_teams_text(self):
        self.__teams_text = "<br>- - - - - - - - - - - - - - - - - - - - results - - - - - - - - - - - - - - - - - - - -<br>"
        self.__teams_text += self.__chime_connection_message
        self.__teams_text += self.__sauna_connection_message
        self.__teams_text += self.__health_check_message
        self.__teams_text += self.__monitor_log_rotation_message
        self.__teams_text += self.__alert_log_rotation_message
        self.__teams_text += self.__notes
    

    def get_last_lines(self, file_path, n):
        try:
            with open(file_path, 'r') as f:
                return collections.deque(f, n)
        except FileNotFoundError:
            print(f"{file_path} not found.")
            return []

    def get_log_file_path(self, job_name):

        print("-----  get_log_file_path() START  ----- ", job_name)
        dir_name_pattern = r"^2[01][0-9]{2}[01][0-9]"
        file_name_pattern = r"^2[01][0-9]{2}[01][0-9][0-3][0-9]_" + job_name + "_log.csv"
        log_dirs = []
        if job_name == 'alert':
            log_dir_path = self.__alert_log_dir
        else:
            log_dir_path = self.__monitor_log_dir
        if os.path.exists(log_dir_path):
            for i in os.listdir(log_dir_path):
                if os.path.isdir(os.path.join(log_dir_path, i)) and re.search(dir_name_pattern, i):
                    log_dirs.append(i)
        target_dir = max(log_dirs)
        print("log_dirs", log_dirs)
        print("target_dir", target_dir)
        target_path = os.path.join(log_dir_path, target_dir)
        file_list = []
        for i in os.listdir(target_path):
            if re.search(file_name_pattern, i):
                file_list.append(i)
        print("file_list", file_list)
        target_file = max(file_list)
        target_file_path = os.path.join(target_path, target_file)
        print("target_file_path", target_file_path)
        print("-----  get_log_file_path() END  ----- ", job_name)
        return target_file_path


    def sauna_current_connection(self):

        print("-----  sauna_current_connection check START  -----")

        prefix = "[Connection] - sauna rooms: "
        message = "ok<br>"
        connection_errors = ""

        for i in range(len(self.__HOSTS_FILES)):
            with open(self.__HOSTS_FILES[i], "r") as f:
                hosts = json.load(f)
            for room in hosts:
                if hosts[room]['status'] == "Connection Error":
                    connection_errors += room + "<br>"
        if connection_errors:
            message = "Warning. Connection Error detected in the next sauna room.<br>" + connection_errors
        print("Connection Errors", connection_errors)
        self.__sauna_connection_message = prefix + message

        print("-----  sauna_current_connection check END  -----")


    def chime_connection(self):
        last_lines = self.get_last_lines()


    def health_check(self, job_name):

        print("-----  health check START  ----- ", job_name)
        if job_name == 'alert':
            index = 0
            threshold = self.__alert_witness_threshold
        else:
            index = 3
            threshold = self.__monitor_witness_threshold

        target_file_path = self.get_log_file_path(job_name)
        last_line = self.get_last_lines(target_file_path, 1)
        last_updated = last_line[0].split(',')[index].replace('/', '-')
        time_diff = (datetime.now() - datetime.strptime(last_updated, '%Y-%m-%d %H:%M:%S')).total_seconds()
        print("time_diff", time_diff)
        print("type(time_diff)", type(time_diff))
        print("int(time_diff)", int(time_diff))

        prefix = "[Health check] - " + job_name + ": "
        message = "ok<br>"
        if time_diff > threshold:
            message = "Warning. " + str(int(time_diff)) + " seconds have passed since the last log.<br>"

        self.__health_check_message += prefix + message
        print("-----  health check END  ----- ", job_name)


    def log_rotation(self, app_name):
        
        print("-----  log_rotation check START  ----- ", app_name)

        if app_name == 'monitor':
            file_path = self.__monitor_log_rotation_log
        else:
            file_path = self.__alert_log_rotation_log

        if os.path.exists(file_path):
            last_line = self.get_last_lines(file_path, 1)
            date_time = last_line[0].split(',')[0].replace('/', '-')
            time_diff = (datetime.now() - datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')).total_seconds() / 60
            print("last_line", last_line)
            print("type(last_line)", type(last_line))
            print("last_line[0]", last_line[0])
            print("time_diff", time_diff)
            print("type(time_diff)", type(time_diff))
            print("int(time_diff)", int(time_diff))

        prefix = "[Health check] - log_rotator - " + app_name + ": "

        message = "ok<br>"
        if os.path.exists(file_path) and time_diff > 70:
            message = "Warning. " + str(int(time_diff)) + " minutes have passed since the last log rotation. Log rotation is executed once every 60 minutes.<br>"

        if app_name == 'monitor':
            self.__monitor_log_rotation_message = prefix + message
        else:
            self.__alert_log_rotation_message = prefix + message
        print("-----  log_rotation check END  ----- ", app_name)

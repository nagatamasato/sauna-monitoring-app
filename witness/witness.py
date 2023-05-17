from datetime import datetime
import json
import os
import pymsteams
import collections
import re


class Witness:

    def __init__(self):
        # Webhook URL
        self.__TEAMS_URL = "https://x1studiocojp.webhook.office.com/webhookb2/2359c523-6ff7-4e43-9cce-b924c34b9a1b@3e594155-a0af-40ef-a8f2-dc8ce23f3844/IncomingWebhook/5798f01fbb53408ea38a9651139d18ea/4eb77287-1789-4810-b206-e1c3bd304107"
        self.__teams_text = ""
        self.__HOSTS_FILES = [
            "..\\hosts_1.json",
            "..\\hosts_2.json",
            "..\\hosts_3.json"
        ]

        # monitor
        self.__monitor_log_dir = "..\\monitor\\logs"
        self.__monitor_1_message = ""
        self.__monitor_2_message = ""
        self.__monitor_3_message = ""

        # alert
        self.__alert_log_dir = "..\\alert\\logs"
        self.__alert_message = ""

        # log rotation - monitor
        self.__monitor_log_rotation_log = "..\\log_rotator\\logs\\monitor-log_rotator-log.csv"
        self.__monitor_log_rotation_message = ""

        # log rotation - alert
        self.__alert_log_rotation_log = "..\\log_rotator\\logs\\alert-log_rotator-log.csv"
        self.__alert_log_rotation_message = ""

        # connection error
        self.__connection_message = ""


    def report(self):
        teams_message = pymsteams.connectorcard(self.__TEAMS_URL)
        teams_message.title("TEST on Development Environment")
        self.get_teams_text()
        teams_message.text(self.__teams_text)
        teams_message.send()


    def get_teams_text(self):
        self.__teams_text = self.__connection_message + self.__alert_message + self.__monitor_log_rotation_message + self.__alert_log_rotation_message
    

    def get_last_lines(self, file_path, n):
        try:
            with open(file_path, 'r') as f:
                return collections.deque(f, n)
        except FileNotFoundError:
            print(f"{file_path} not found.")
            return []


    def sauna_current_connection(self):

        prefix = "Connection - Sauna rooms: "
        message = "ok<br>"
        connection_errors = ""

        for i in range(len(self.__HOSTS_FILES)):
            with open(self.__HOSTS_FILES[i], "r") as f:
                hosts = json.load(f)
            for room in hosts:
                if hosts[room]['status'] == "Connection Error":
                    connection_errors += room + "<br>"
        if connection_errors:
            message = "Hi, I got a Connection Error in the next sauna room.<br>" + connection_errors
        print("Connection Errors", connection_errors)
        self.__connection_message = prefix + message


    def monitor_1(self):
        # file_name = self.__monitor_log + "\\202305\\" + "20230515_monitor_1_log.csv"
        file_path = "..\\monitor\\logs\\202305\\20230515_monitor_1_log.csv"
        print("file_name", file_path)
        last_line = self.get_last_lines(file_path, 1)
        print("last_line", last_line)
        print("type(last_line)", type(last_line))
        print("last_line[0]", last_line[0])
        with open(".\\test.txt", "a") as f:
            f.write(last_line[0])
        print("last_line", last_line)
        print(type(last_line))
        date_time = last_line[0].split(',')[3].replace('/', '-')
        print("date_time", date_time)
        time_diff = (datetime.now() - datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')).total_seconds()
        print("time_diff", time_diff)
        if time_diff > 10:
            self.__monitor_1_message = "Error, Update time has not been updated for 10 seconds.<br>"
    

    def monitor_2(self):
        self.__monitor_2_message = ""


    def monitor_3(self):
        self.__monitor_3_message = ""
    

    def alert(self):

        dir_name_pattern = r"^2[01][0-9]{2}[01][0-9]"
        file_name_pattern = r"^2[01][0-9]{2}[01][0-9][0-3][0-9]_alert_log.csv"
        log_dirs = []
        if os.path.exists(self.__alert_log_dir):
            for i in os.listdir(self.__alert_log_dir):
                if os.path.isdir(os.path.join(self.__alert_log_dir, i)) and re.search(dir_name_pattern, i):
                    log_dirs.append(i)
        target_dir = max(log_dirs)
        print("log_dirs", log_dirs)
        print("target_dir", target_dir)
        target_path = os.path.join(self.__alert_log_dir, target_dir)
        file_list = []
        for i in os.listdir(target_path):
            if re.search(file_name_pattern, i):
                file_list.append(i)
        print("file_list", file_list)
        target_file = max(file_list)
        target_file_path = os.path.join(target_path, target_file)
        print("target_file_path", target_file_path)
        last_line = self.get_last_lines(target_file_path, 1)
        last_updated = last_line[0].split(',')[0].replace('/', '-')
        time_diff = (datetime.now() - datetime.strptime(last_updated, '%Y-%m-%d %H:%M:%S')).total_seconds()

        prefix = "Health check - alert: "
        message = "ok<br>"
        if time_diff > 5:
            message = "Warning. 5 seconds have passed since the last alert log.<br>"
            
        self.__alert_message = prefix + message


    def log_rotation(self, app_name):

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

        prefix = "Log rotation - " + app_name + ": "

        message = "ok<br>"
        if os.path.exists(file_path) and time_diff > 70:
            message = "Warning. 70 minutes have passed since the last log rotation. Log rotation is executed once every 60 minutes.<br>"

        if app_name == 'monitor':
            self.__monitor_log_rotation_message = prefix + message
        else:
            self.__alert_log_rotation_message = prefix + message

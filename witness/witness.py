from datetime import datetime
import json
import os
import pymsteams


class Witness:

    def __init__(self):
        # Webhook URL
        self.__TEAMS_URL = "https://x1studiocojp.webhook.office.com/webhookb2/2359c523-6ff7-4e43-9cce-b924c34b9a1b@3e594155-a0af-40ef-a8f2-dc8ce23f3844/IncomingWebhook/5798f01fbb53408ea38a9651139d18ea/4eb77287-1789-4810-b206-e1c3bd304107"
        self.__HOSTS_FILES = [
            "..\\hosts_1.json",
            "..\\hosts_2.json",
            "..\\hosts_3.json"
        ]

        # monitor
        self.__monitor_log = "..\\monitor\\logs"
        self.__monitor_1_message = ""
        self.__monitor_2_message = ""
        self.__monitor_3_message = ""

        # alert
        self.__alert_log = "..\\alert\\logs"
        self.__alert_message = ""

        # log rotation
        self.__monitor_log_rotation_log = "..\\log_rotator\\logs"
        self.__alert_log_rotation_log = ""
        self.__log_rotation_message = ""

        # connection error
        self.__connection_message = ""


    def get_last_line(file_name):
        with open(file_name, 'rb') as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            last_line = f.readline().decode()
        return last_line


    def connection_check(self):

        self.__connection_message = "Hi, Sauna Emergency App is working fine."
        connection_errors = ""

        for i in range(len(self.__HOSTS_FILES)):
            with open(self.__HOSTS_FILES[i], "r") as f:
                hosts = json.load(f)

            for room in hosts:
                if hosts[room]['status'] == "Connection Error":
                    self.__connection_message = "Hi, I got a Connection Error in the next sauna room.<br>"
                    connection_errors += room + "<br>"
        print("Connection Errors", connection_errors)
        self.__connection_message += connection_errors


    def monitor_1_check(self):
        # file_name = self.__monitor_log + "\\202305\\" + "20230515_monitor_1_log.csv"
        file_name = "..\\monitor\\logs\\202305\\20230515_monitor_1_log.csv"
        print("file_name", file_name)
        last_line = Witness.get_last_line(file_name)
        with open(".\\test.txt", "a") as f:
            f.write(last_line)
        print("last_line", last_line)
        print(type(last_line))
        date_time = last_line.split(',')[3].replace('/', '-')
        print("date_time", date_time)
        time_diff = (datetime.now() - datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')).total_seconds()
        print("time_diff", time_diff)
        if time_diff > 10:
            self.__monitor_1_message = "Error, Update time has not been updated for 10 seconds.<br>"
    

    def monitor_2_check(self):
        self.__monitor_2_message = ""


    def monitor_3_check(self):
        self.__monitor_3_message = ""
    

    def alert_cehck(self):
        self.__alert_message = ""


    def log_rotation_check(self):
        self.__log_rotation_message = ""


    def report(self):
        teams_message = pymsteams.connectorcard(self.__TEAMS_URL)
        teams_message.title("TEST on Development Environment")
        teams_message.text(self.__connection_message)
        teams_message.send()

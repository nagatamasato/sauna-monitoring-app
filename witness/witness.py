from datetime import datetime
import json
import os
import requests
import collections
import re


class Witness:

    def __init__(self):
        # Teams Webhook
        self.__WEBHOOK_URL = "https://x1studiocojp.webhook.office.com/webhookb2/2359c523-6ff7-4e43-9cce-b924c34b9a1b@3e594155-a0af-40ef-a8f2-dc8ce23f3844/IncomingWebhook/5798f01fbb53408ea38a9651139d18ea/4eb77287-1789-4810-b206-e1c3bd304107"
        self.__mention = False
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
        self.__notes = '''\n\n= = = = = = = = = = = = = = = = = = = = = = notes = = = = = = = = = = = = = = = = = = = = = =\n\n
        [Connection]:\n\n
            Check if a timeout has occurred. Timeout threshold is {} second.\n\n
        \n\n
        [Health check]:\n\n
            Verify that the script is working properly\n\n
            by checking if the log update date/time is updated within the threshold.\n\n
            The thresholds are as follows\n\n
                ・monitor_[1-3]: {} seconds\n\n
                ・alert: {} seconds\n\n
                ・log_rotator: {} minutes\n\n
        '''.format(
            self.__timeout_threshold,
            self.__monitor_witness_threshold,
            self.__alert_witness_threshold,
            self.__log_rotator_witness_threshold
        )

        #health check
        self.__health_check_message = ""
        self.__monitor_log_dir = "..\\monitor\\logs"
        self.__alert_log_dir = "..\\alert\\logs"
        self.__monitor_log_file_paths = {
            'monitor_1': self.get_log_file_path('monitor_1'),
            'monitor_2': self.get_log_file_path('monitor_2'),
            'monitor_3': self.get_log_file_path('monitor_3')
        }
        self.__alert_log_file_path = self.get_log_file_path('alert')

        # log rotation - monitor
        self.__monitor_log_rotation_log = "..\\log_rotator\\logs\\monitor-log_rotator-log.csv"
        self.__monitor_log_rotation_message = ""

        # log rotation - alert
        self.__alert_log_rotation_log = "..\\log_rotator\\logs\\alert-log_rotator-log.csv"
        self.__alert_log_rotation_message = ""

        # connection
        self.__sauna_current_connection_message = ""
        self.__sauna_error_count_message = ""
        self.__chime_connection_message = ""

    def report(self):

        self.get_teams_text()
        # アダプティブカードのJSONを定義
        mention_card = {
            "type": "message",
            "attachments": [
                {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "body": [
                        {
                            "type": "TextBlock",
                            "size": "Medium",
                            "weight": "Bolder",
                            "text": "Sample Adaptive Card with User Mention"
                        },
                        {
                            "type": "TextBlock",
                            "text": "<at>Masato Nagata</at>\n\n\
                                This is TEST on Development Environment\n\n"\
                                    + self.__teams_text
                        }
                    ],
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.0",
                    "msteams": {
                        "width": "Full",
                        "entities": [
                            {
                                "type": "mention",
                                "text": "<at>Masato Nagata</at>",
                                "mentioned": {
                                "id": "nagata-m@x1studio.co.jp",
                                "name": "Masato Nagata"
                                }
                            }
                        ]
                    }
                }
            }]
        }

        not_mention_card = {
            "type": "message",
            "attachments": [
                {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "body": [
                        {
                            "type": "TextBlock",
                            "size": "Medium",
                            "weight": "Bolder",
                            "text": "Sample Adaptive Card with User Mention"
                        },
                        {
                            "type": "TextBlock",
                            "text": "This is TEST on Development Environment\n\n"\
                                    + self.__teams_text
                        }
                    ],
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.0",
                    "msteams": {
                        "width": "Full"
                    }
                }
            }]
        }

        # ヘッダーとペイロードを定義
        headers = {
            'Content-Type': 'application/json'
        }

        # mention
        if self.__mention:
            card = mention_card
        else:
            card = not_mention_card

        # POSTリクエストを送信
        response = requests.post(self.__WEBHOOK_URL, headers=headers, data=json.dumps(card))

        # 応答を表示
        print(response.status_code)


    def get_teams_text(self):
        self.__teams_text = "\n\n= = = = = = = = = = = = = = = = = = = = = = results = = = = = = = = = = = = = = = = = = = = = =\n\n"
        self.__teams_text += self.__chime_connection_message\
            + self.__sauna_current_connection_message + '\n\n'\
            + self.__sauna_error_count_message + '\n\n'\
            + self.__health_check_message\
            + self.__monitor_log_rotation_message\
            + self.__alert_log_rotation_message\
            + self.__notes
    

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

        prefix = "[Connection] - Current connection status of sauna rooms: "
        message = "ok\n\n"
        connection_errors = []
        suffix = ", "

        for i in range(len(self.__HOSTS_FILES)):
            with open(self.__HOSTS_FILES[i], "r") as f:
                hosts = json.load(f)
            for room in hosts:
                if hosts[room]['status'] == "Failure to get status":
                    connection_errors.append(room)
        if connection_errors:
            message = "Warning. Failure to get status detected in the next sauna room.\n\n"
            for j in range(len(connection_errors)):
                if j == len(connection_errors) - 1:
                    suffix = ""
                message += connection_errors[j] + suffix
        print("Failure to get status", connection_errors)
        self.__sauna_current_connection_message = prefix + message + '\n\n'
        print("-----  sauna_current_connection check END  -----")


    def sauna_error_count(self):

        print("-----  sauna_error_count() START  -----")
        count = {}
        for monitor_name in self.__monitor_log_file_paths:
            print("monitor_name", monitor_name)
            if monitor_name == 'monitor_1':
                n = 3 * 10 * 5
            else:
                n = 4 * 10 * 5
            last_lines = self.get_last_lines(self.__monitor_log_file_paths[monitor_name], n)
            print("last_lines)", last_lines)
            for i in range(len(last_lines)):
                print("last_lines[i]", last_lines[i])
                line_list = last_lines[i].split(',')
                print("line_list", line_list)
                print("type(line_list)", type(line_list))
                count.setdefault(line_list[0], 0)
                if line_list[1] == 'Failure to get status':
                    count[line_list[0]] += 1
                    print("line_list", line_list)
                    print("count[line_list[0]]", count[line_list[0]])
                    print("count", count)
        prefix = '[Connection]: Number of "Failure to get status" in sauna rooms for approximately 5 minutes is as follows\n\n'
        message = ""
        suffix = ", "
        count_sorted = sorted(count.items())
        print("count_sorted", count_sorted)
        print("type(count_sorted)", type(count_sorted))
        for i in range(len(count_sorted)):
            print("count_sorted[i]", count_sorted[i])
            print("type(count_sorted[i])", type(count_sorted[i]))
            print("count_sorted[i][0]", count_sorted[i][0])
            print("type(count_sorted[i][0])", type(count_sorted[i][0]))
            print("count_sorted[i][1]", count_sorted[i][1])
            print("type(count_sorted[i][1])", type(count_sorted[i][1]))
            if i == len(count_sorted) - 1:
                suffix = ""
            message += count_sorted[i][0] + ": " + str(count_sorted[i][1]) + suffix
        self.__sauna_error_count_message = prefix + message + '\n\n'
        print(self.__sauna_error_count_message)
        print("-----  sauna_error_count() END  -----")


    def chime_error_count(self):

        print("-----  chime_error_count() START  -----")
        last_lines = self.get_last_lines(self, self.__alert_log_file_path, 4)
        log = last_lines[0]
        print("last_lines", last_lines)
        print("last_lines[0]", last_lines[0])
        if True:
            self.__chime_connection_message = ""
        print("-----  chime_error_count() END  -----")


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
        last_updated = last_line[0].split(',')[index]
        time_diff = (datetime.now() - datetime.strptime(last_updated, '%Y-%m-%d %H:%M:%S')).total_seconds()
        print("time_diff", time_diff)
        print("type(time_diff)", type(time_diff))
        print("int(time_diff)", int(time_diff))

        prefix = "[Health check] - " + job_name + ": "
        message = "ok\n\n"
        if time_diff > threshold:
            message = "Warning. " + str(int(time_diff)) + " seconds have passed since the last log.\n\n"

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
            date_time = last_line[0].split(',')[0]
            print("date_time", date_time)
            print("type(date_time)", type(date_time))
            time_diff = (datetime.now() - datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')).total_seconds() / 60
            print("last_line", last_line)
            print("type(last_line)", type(last_line))
            print("last_line[0]", last_line[0])
            print("time_diff", time_diff)
            print("type(time_diff)", type(time_diff))
            print("int(time_diff)", int(time_diff))

        prefix = "[Health check] - log_rotator - " + app_name + ": "

        message = "ok\n\n"
        if os.path.exists(file_path) and time_diff > 70:
            message = "Warning. " + str(int(time_diff)) + " minutes have passed since the last log rotation. Log rotation is executed once every 60 minutes.\n\n"

        if app_name == 'monitor':
            self.__monitor_log_rotation_message = prefix + message
        else:
            self.__alert_log_rotation_message = prefix + message
        print("-----  log_rotation check END  ----- ", app_name)

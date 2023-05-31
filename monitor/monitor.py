from telnetlib import Telnet
from datetime import datetime
import json
import logging
from logging.handlers import RotatingFileHandler
import os
import re
import time
import sys
sys.path.append('..\\common')
from path_generator import PathGenerator
sys.path.append('..\\view')
from generate_html import GenerateHtml


class Monitor:

    def __init__(self, job_name, json_path):

        self.job_name = job_name
        self.json_path = json_path
        self.__PORT = 23
        self.__USER = "x1s"
        self.__PASSWORD = "Admin12345"
        self.__GET_STATUS_COMMAND = "?SYSVAR,4,1"
        self.__pattern = r"^~SYSVAR,4,1,[01]"
        self.__timeout_threshold = 1

        path_generator = PathGenerator(self.job_name)
        self.__LOG_PATH = path_generator.create_path()

        self.__logging_file = '..\\app_logs\\' + job_name + '.log'
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = RotatingFileHandler(self.__logging_file, maxBytes= 100 * 1024 * 1024 , backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)


    def get_formatted_datetime(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    def get_status(self):

        print("get_status START")
        self.logger.info('get_status START')

        write_header = False

        if not os.path.exists(self.__LOG_PATH):
            write_header = True

        try:
            with open(self.__LOG_PATH, "a") as f:
                if write_header:
                    header = "Room,Status,Emergency_time,Updated_time,Host\n"
                    f.write(header)
                    write_header = False

                with open(self.json_path, "r") as jsonf:
                    hosts = json.load(jsonf)
                    
                for i in hosts:
                    # start Telnet session
                    try:
                        tn = Telnet(hosts[i]['host'], self.__PORT, timeout=self.__timeout_threshold)
                        tn.read_until(b"login: ")
                        tn.write(self.__USER.encode("utf-8") + b"\r\n")
                        tn.read_until(b"password: ")
                        tn.write(self.__PASSWORD.encode("utf-8") + b"\r\n")
                        tn.read_until(b"QNET> ")
                        tn.write(self.__GET_STATUS_COMMAND.encode("utf-8") + b"\r\n")
                        result = tn.read_until(b"QNET> ")
                        print("result_1", result)
                        self.logger.debug("result_1: %s", result)
                        result = result.decode("utf-8")
                        print("result_2", result)
                        self.logger.debug("result_2: %s", result)
                        result = result.replace("QNET> ", "")
                        print("result_3", result)
                        self.logger.debug("result_3: %s", result)
                        result = result.replace("\n", "")
                        print("result_4", result)
                        self.logger.debug("result_4: %s", result)
                        result = result.splitlines()
                        print("result_5", result)
                        self.logger.debug("result_5: %s", result)
                        target = ""
                        for j in range(len(result)):
                            if re.search(self.__pattern, result[j]):
                                target = result[j]
                                break
                        print("target", target)
                        self.logger.debug("target: %s", target)
                        result = target
                        if result:
                            result = result.split(',')
                            print("result_6", result)
                            self.logger.debug("result_6: %s", result)
                            result = result[3]
                            print("result_7", result)
                            self.logger.debug("result_7: %s", result)
                        else:
                            result = "Failure to get status"
                            print("Failed to get target")
                            self.logger.debug("Failed to get target")

                    except Exception as e:
                        result = "Failure to get status"
                        self.logger.exception("An error occurred: %s", str(e))

                    current_status = result
                    print("current_status", current_status)
                    self.logger.debug("current_status: %s", current_status)

                    now = self.get_formatted_datetime()
                    print("current time: ", now)
                    self.logger.debug("current_time: %s", now)
    
                    with open(self.json_path, "r") as jsonf:
                        hosts = json.load(jsonf)

                    print("statuses", hosts)
                    self.logger.debug("statuses: %s", hosts)
                    print("old_status", hosts[i]['status'])
                    self.logger.debug("old_status: %s", hosts[i]['status'])
                    print("new_status", current_status)
                    self.logger.debug("new_status: %s", current_status)

                    hosts[i]['status'] = current_status

                    # 緊急ボタンONを最初に検知した時刻をセット
                    if hosts[i]['status'] == '1' and hosts[i]['emergency_time'] == "":
                        hosts[i]['emergency_time'] = now
                        hosts[i]['history'].append(now)

                    # 緊急ボタンOFFを検知した場合は空欄に戻す
                    if hosts[i]['status'] == '0':
                        hosts[i]['emergency_time'] = ""

                    hosts[i]['updated_time'] = now

                    with open(self.json_path, "w") as jsonf:
                        json.dump(hosts, jsonf)

                    emergency_time = hosts[i]['emergency_time']
                    log = i + "," + current_status + "," + emergency_time + "," + now + "," + hosts[i]['host'] + "\n"
                    f.write(log)

                    view = GenerateHtml()
                    view.monitoring()
                    view.history()

                    # terminate Telnet session
                    try:
                        tn.write(b"exit\n")
                        self.logger.info('telnet session terminated')
                        time.sleep(1)
                    except Exception as e:
                        self.logger.exception("An error occurred: %s", str(e))


            print("get_status END")
            self.logger.info('get_status END')
        
        except Exception as e:
            self.logger.exception("An error occurred: %s", str(e))


    def monitoring(self):

        # 定期実行間隔
        INTERVAL = 60
        # 1回のINTERVAL中の実行回数
        FREQUENCY = 10
        # 実行時間がINTERVAL(60秒)を超えないように設定
        MARGIN = 0.05
        # １回あたりの最大時間
        MAXTIME = (INTERVAL / FREQUENCY) - MARGIN

        start_time = datetime.now()
        print("start_time", start_time)
        self.logger.debug("start_time: %s", start_time)

        for i in range(FREQUENCY):
            print(i + 1, "/", FREQUENCY)
            self.logger.info("%i/%i", i, FREQUENCY)
            # 開始時刻
            start = datetime.now()
            # サウナルームのステータスを取得
            self.get_status()
            # 終了時刻
            end = datetime.now()
            # 実行時間
            runtime = (end - start).total_seconds()

            print("start", start)
            self.logger.debug("start: %s", start)
            print("end", end)
            self.logger.debug("end: %s", end)
            print("runtime", runtime)
            self.logger.debug("runtime: %s", runtime)

            wait = MAXTIME - runtime
            print("wait", wait)
            self.logger.debug("wait: %s", wait)
            if (wait > 0):
                time.sleep(wait)

            end_time = datetime.now()
            total_time = (end_time - start_time).total_seconds()
            print("end_time", end_time)
            self.logger.debug("end_time: %s", end_time)
            print("total_time", total_time)
            self.logger.debug("total_time: %s", total_time)

from telnetlib import Telnet
from datetime import datetime
import json
import logging
from logging.handlers import RotatingFileHandler
import os
import time
import sys
sys.path.append('..\\common')
from path_generator import PathGenerator


class Alert:

    def __init__(self):

        self.job_name = "alert"
        self.__HOST = "192.168.10.231"
        self.__PORT = 23
        self.__USER = "x1s"
        self.__PASSWORD = "Admin12345"
        self.__ALERT_ON_COMMAND = "#OUTPUT,6,1,1"
        self.__ALERT_OFF_COMMAND = "#OUTPUT,6,1,0"
        self.__timeout_threshold = 1

        path_generator = PathGenerator(self.job_name)
        self.__LOG_PATH = path_generator.create_path()

        self.__logging_file = '..\\app_logs\\' + self.job_name + '.log'
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = RotatingFileHandler(self.__logging_file, maxBytes= 100 * 1024 * 1024 , backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)


    def get_formatted_datetime(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    

    def alert(self):

        print("alert START")
        self.logger.info('alert START')
        try:
            # Telnet session start
            self.logger.info('telnet session start')
            tn = Telnet(self.__HOST, self.__PORT, timeout=self.__timeout_threshold)
            tn.read_until(b"login: ")
            tn.write(self.__USER.encode("UTF-8") + b"\r\n")
            tn.read_until(b"password: ")
            tn.write(self.__PASSWORD.encode("UTF-8") + b"\r\n")
            tn.read_until(b"QNET> ")

            with open(self.__LOG_PATH, "a") as f:
                f.write(self.get_formatted_datetime() + ",ping-pong START\n")
                print('ping-pong START')
                self.logger.info('ping-pong START')
                for i in range(14):
                    tn.write(self.__ALERT_ON_COMMAND.encode("UTF-8") + b"\r\n")
                    f.write(self.get_formatted_datetime() + ",ping " + str(i) + '\n')
                    print('ping', i)
                    self.logger.info('ping ' + str(i))
                    time.sleep(2)
                    tn.write(self.__ALERT_OFF_COMMAND.encode("UTF-8") + b"\r\n")
                    f.write(self.get_formatted_datetime() + ",pong " + str(i) + '\n')
                    print('pong', i)
                    self.logger.info('pong ' + str(i))
                    time.sleep(2)
                f.write(self.get_formatted_datetime() + ",ping-pong END\n")
                print('ping-pong END')
                self.logger.info('ping-pong END')

        except Exception as e:
            with open(self.__LOG_PATH, "a") as f:
                f.write(self.get_formatted_datetime() + ",Failed to chime in.\n")
            self.logger.exception("An error occurred: %s", str(e))

        # terminate Telnet session
        try:
            tn.write(b"exit\n")
            self.logger.info('telnet session terminated')
            sys.exit()

        except Exception as e:
            self.logger.exception("An error occurred: %s", str(e))

        print("alert END")
        self.logger.info('alert END')


    def check_emergency(self, hosts_file):

        try:
            with open(hosts_file, "r") as f:
                hosts = json.load(f)

        except Exception as e:
            self.logger.exception("An error occurred: %s", str(e))

        emergency_rooms = ""
        failures = ""
        normal_rooms = ""
        for room in hosts:
            if hosts[room]['status'] == "1":
                emergency_rooms += room + " "
            elif hosts[room]['status'] == "Failure to get status":
                failures += room + " "
            else:
                normal_rooms += room + " "
        print('emergency_rooms', emergency_rooms)
        print('failures', failures)
        print('normal_rooms', normal_rooms)
        self.logger.debug("emergency_rooms: %s", emergency_rooms)
        self.logger.debug("failures: %s", failures)
        self.logger.debug("normal_rooms: %s", normal_rooms)

        write_header = False
        if not os.path.exists(self.__LOG_PATH):
            write_header = True

        try:
            with open(self.__LOG_PATH, "a") as f:
                if write_header:
                    header = "Datetime,Message\n"
                    f.write(header)
                    write_header = False
                now = self.get_formatted_datetime()
                if emergency_rooms:
                    log = now + ",The following is Emergency " + emergency_rooms + "\n"
                elif failures:
                    log = now + ",The following is Failure to get status " + failures + "\n"
                else:
                    log = now + ",The following is Normal " + normal_rooms + "\n"
                f.write(log)

        except Exception as e:
            self.logger.exception("An error occurred: %s", str(e))

        if emergency_rooms:
            self.alert()

from telnetlib import Telnet
from datetime import datetime
import json
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


    def get_formatted_datetime(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    

    def alert(self):

        print("alert START")
        try:
            # Telnetセッションを開始
            tn = Telnet(self.__HOST, self.__PORT, timeout=self.__timeout_threshold)
            tn.read_until(b"login: ")
            tn.write(self.__USER.encode("UTF-8") + b"\r\n")
            tn.read_until(b"password: ")
            tn.write(self.__PASSWORD.encode("UTF-8") + b"\r\n")
            tn.read_until(b"QNET> ")

            with open(self.__LOG_PATH, "a") as f:
                try:
                    f.write(self.get_formatted_datetime() + ",ping-pong START\n")
                    for i in range(14):
                        tn.write(self.__ALERT_ON_COMMAND.encode("UTF-8") + b"\r\n")
                        f.write(self.get_formatted_datetime() + ",ping\n")
                        time.sleep(2)
                        tn.write(self.__ALERT_OFF_COMMAND.encode("UTF-8") + b"\r\n")
                        f.write(self.get_formatted_datetime() + ",pong\n")
                        time.sleep(2)
                    f.write(self.get_formatted_datetime() + ",ping-pong END\n")
                except:
                    f.write(self.get_formatted_datetime() + ",Failed to chime in.\n")
                    print("Failed to chime in")
        except:
            with open(self.__LOG_PATH, "a") as f:
                f.write(self.get_formatted_datetime() + ",Failed to chime in.\n")
        print("alert END")


    def check_emergency(self, hosts_file):

        with open(hosts_file, "r") as f:
            hosts = json.load(f)

        print("hosts", hosts)

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

        with open(self.__LOG_PATH, "a") as f:
            now = self.get_formatted_datetime()
            if emergency_rooms:
                log = now + ",The following is Emergency " + emergency_rooms + "\n"
            elif failures:
                log = now + ",The following is Failure to get status " + failures + "\n"
            else:
                log = now + ",The following is Normal " + normal_rooms + "\n"
            f.write(log)

        if emergency_rooms:
            self.alert()

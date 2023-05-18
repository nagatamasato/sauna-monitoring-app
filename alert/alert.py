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

        path_generator = PathGenerator(self.job_name)
        self.__LOG_PATH = path_generator.create_path()


    def alert(self):

        print("alert START")

        try:
            # Telnetセッションを開始
            tn = Telnet(self.__HOST, self.__PORT, timeout=1)
            tn.read_until(b"login: ")
            tn.write(self.__USER.encode("UTF-8") + b"\r\n")
            tn.read_until(b"password: ")
            tn.write(self.__PASSWORD.encode("UTF-8") + b"\r\n")
            tn.read_until(b"QNET> ")

            with open(self.__LOG_PATH, "a") as f:
                now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                start = now + ",alert START\n"
                f.write(start)
                
            for i in range(14):
                # ALERT_ON
                tn.write(self.__ALERT_ON_COMMAND.encode("UTF-8") + b"\r\n")
                time.sleep(2)
                tn.write(self.__ALERT_OFF_COMMAND.encode("UTF-8") + b"\r\n")
                time.sleep(2)

            with open(self.__LOG_PATH, "a") as f:
                now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                end = now + ",alert END\n"
                f.write(end)

            # Telnetセッションを終了
            tn.write(b"exit\r\n")
        
        except:
            with open(self.__LOG_PATH, "a") as f:
                now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                connection_error = now + ",Connection Error. Can't ring the chime.\n"
                f.write(connection_error)
                print("Connection Error")
        
        print("alert END")


    def check_emergency(self, hosts_file):

        with open(hosts_file, "r") as f:
            hosts = json.load(f)

        print("hosts", hosts)

        emergency_rooms = ""
        connection_errors = ""
        normal_rooms = ""
        for room in hosts:
            if hosts[room]['status'] == "1":
                emergency_rooms += room + " "
            elif hosts[room]['status'] == "Connection Error":
                connection_errors += room + " "
            else:
                normal_rooms += room + " "

        with open(self.__LOG_PATH, "a") as f:
            now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            if emergency_rooms:
                log = now + ",The following is Emergency " + emergency_rooms + "\n"
            elif connection_errors:
                log = now + ",The following is Connection Error " + connection_errors + "\n"
            else:
                log = now + ",The following is Normal " + normal_rooms + "\n"
            f.write(log)

        if emergency_rooms:
            self.alert()

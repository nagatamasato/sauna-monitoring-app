from telnetlib import Telnet
from datetime import datetime
import json
import time
import sys
sys.path.append('..\\common')
from path_generator import PathGenerator


class Alert:

    def __init__(self):

        self.job = "alert"
        self.__HOST = "192.168.10.231"
        self.__PORT = 23
        self.__USER = "x1s"
        self.__PASSWORD = "Admin12345"
        self.__ALERT_ON_COMMAND = "#OUTPUT,6,1,1"
        self.__ALERT_OFF_COMMAND = "#OUTPUT,6,1,0"

        path_generator = PathGenerator(self.job)
        self.__PATH = path_generator.create_path()


    def alert(self):

        print("alert START")

        

        try:
            # Telnetセッションを開始
            tn = Telnet(Alert.__HOST, self.__PORT, timeout=5)
            tn.read_until(b"login: ")
            tn.write(self.__USER.encode("UTF-8") + b"\r\n")
            tn.read_until(b"password: ")
            tn.write(self.__PASSWORD.encode("UTF-8") + b"\r\n")
            tn.read_until(b"QNET> ")

            with open(self.__PATH, "a") as f:
                now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                start = now + ",alert START\n"
                f.write(start)
                
            for i in range(25):
                # ALERT_ON
                tn.write(self.__ALERT_ON_COMMAND.encode("UTF-8") + b"\r\n")
                # 2秒待つ
                time.sleep(2)
                # ALERT_OFF
                tn.write(self.__ALERT_OFF_COMMAND.encode("UTF-8") + b"\r\n")

            with open(self.__PATH, "a") as f:
                now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                end = now + ",alert END\n"
                f.write(end)

            # Telnetセッションを終了
            tn.write(b"exit\r\n")
        
        except:
            with open(self.__PATH, "a") as f:
                now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                connection_error = now + ",connection error\n"
                f.write(connection_error)
                print("connection error")
        
        print("alert END")


    def check_emergency(self, path):

        with open(path, "r") as f:
            hosts = json.load(f)

        print("hosts", hosts)

        emergencies = {}
        for i in hosts:
            if hosts[i]['status'] == "1":
                emergencies[i] = hosts[i]

        print("emergencies", emergencies) 

        if (emergencies):
            self.alert()

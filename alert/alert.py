from telnetlib import Telnet
from datetime import datetime
import json
import time
import sys
sys.path.append('..\\common')
from path_generator import PathGenerator


class Alert:

    __APP_NAME = "alert"
    __HOST = "192.168.10.231"
    __PORT = 23
    __USER = "x1s"
    __PASSWORD = "Admin12345"
    __ALERT_ON_COMMAND = "#OUTPUT,6,1,1"
    __ALERT_OFF_COMMAND = "#OUTPUT,6,1,0"
    __PATH = PathGenerator.create_path(__APP_NAME)


    def alert():

        print("alert START")

        

        try:
            # Telnetセッションを開始
            tn = Telnet(Alert.__HOST, Alert.__PORT, timeout=5)
            tn.read_until(b"login: ")
            tn.write(Alert.__USER.encode("UTF-8") + b"\r\n")
            tn.read_until(b"password: ")
            tn.write(Alert.__PASSWORD.encode("UTF-8") + b"\r\n")
            tn.read_until(b"QNET> ")

            with open(Alert.__PATH, "a") as f:
                now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                start = now + ",alert START\n"
                f.write(start)
                
            for i in range(25):
                # ALERT_ON
                tn.write(Alert.__ALERT_ON_COMMAND.encode("UTF-8") + b"\r\n")
                # 2秒待つ
                time.sleep(2)
                # ALERT_OFF
                tn.write(Alert.__ALERT_OFF_COMMAND.encode("UTF-8") + b"\r\n")

            with open(Alert.__PATH, "a") as f:
                now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                end = now + ",alert END\n"
                f.write(end)

            # Telnetセッションを終了
            tn.write(b"exit\r\n")
        
        except:
            with open(Alert.__PATH, "a") as f:
                now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                connection_error = now + ",connection error\n"
                f.write(connection_error)
                print("connection error")
        
        print("alert END")


    def check_emergency(path):

        with open(path, "r") as f:
            hosts = json.load(f)

        print("hosts", hosts)

        emergencies = {}
        for i in hosts:
            if hosts[i]['status'] == "1":
                emergencies[i] = hosts[i]

        print("emergencies", emergencies) 

        if (emergencies):
            Alert.alert()

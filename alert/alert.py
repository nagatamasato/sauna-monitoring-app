from telnetlib import Telnet
from datetime import datetime
import time
import sys
sys.path.append('..\\common')
from log_manager import LogManager


class Alert:

    __APP_NAME = "alert"
    __HOST = "192.168.0.231"
    __PORT = 23
    __USER = "x1s"
    __PASSWORD = "Admin12345"
    __ALERT_ON_COMMAND = "#OUTPUT,6,1,1"
    __ALERT_OFF_COMMAND = "#OUTPUT,6,1,0"
    __PATH = LogManager.create_path(__APP_NAME)


    def alert():

        print("alert START")

        with open(Alert.__PATH, "a") as f:
            now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            start = now + ",alert START\n"
            f.write(start)

        # Telnetセッションを開始
        tn = Telnet(Alert.__HOST, Alert.__PORT)
        tn.read_until(b"login: ")
        tn.write(Alert.__USER.encode("UTF-8") + b"\r\n")
        tn.read_until(b"password: ")
        tn.write(Alert.__PASSWORD.encode("UTF-8") + b"\r\n")
        tn.read_until(b"QNET> ")
        
        for i in range(25):
            tn.write(Alert.__ALERT_ON_COMMAND.encode("UTF-8") + b"\r\n")  # ALERT_ON
            # result = tn.read_until(b"QNET> ")
            # f.write(result.decode("utf-8"))
            time.sleep(2)  # 2秒待つ
            tn.write(Alert.__ALERT_OFF_COMMAND.encode("UTF-8") + b"\r\n")  # ALERT_OFF
            # result = tn.read_until(b"QNET> ")
            # f.write(result.decode("utf-8"))

        # Telnetセッションを終了
        tn.write(b"exit\r\n")

        with open(Alert.__PATH, "a") as f:
            now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            end = now + ",alert END\n"
            f.write(end)
            
        print("alert END")

from telnetlib import Telnet
import time
from create_path import CreatePath


class Alert:

    HOST = "192.168.0.231"
    PORT = 23
    USER = "x1s"
    PASSWORD = "Admin12345"
    ALERT_ON = "#OUTPUT,6,1,1"
    ALERT_OFF = "#OUTPUT,6,1,0"
    PATH = CreatePath.create_path("alert")

    def alert():

        print("alert START")

        with open(Alert.PATH, "w") as f:
            # Telnetセッションを開始
            tn = Telnet(Alert.HOST, Alert.PORT)
            tn.read_until(b"login: ")
            tn.write(Alert.USER.encode("UTF-8") + b"\r\n")
            tn.read_until(b"password: ")
            tn.write(Alert.PASSWORD.encode("UTF-8") + b"\r\n")
            tn.read_until(b"QNET> ")
            
            for i in range(25):
                tn.write(Alert.ALERT_ON.encode("UTF-8") + b"\r\n")  # ALERT_ON
                time.sleep(2)  # 2秒待つ
                tn.write(Alert.ALERT_OFF.encode("UTF-8") + b"\r\n")  # ALERT_OFF
                    
            tn.read_until(b"QNET> ")
            result = result.decode("utf-8")
            result = result.replace("QNET> ", "")
            result = result.replace("\n", "")

            # 結果を取得
            result = tn.read_until(b"QNET> ")
            # 結果をファイルに書き込む
            f.write(result.decode("UTF-8"))
            # Telnetセッションを終了
            tn.write(b"exit\r\n")

        print("alert END")

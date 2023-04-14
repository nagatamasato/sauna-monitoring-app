from telnetlib import Telnet
import time
from create_path import CreatePath
from sauna import Sauna


class Alert:

    HOST = "192.168.0.231"
    PORT = 23
    USER = "x1s"
    PASSWORD = "Admin12345"
    ALERT_ON = "#OUTPUT,6,1,1"
    ALERT_OFF = "#OUTPUT,6,1,0"
    PATH = CreatePath.create_path("run_alert")

    def alert(emergency_hosts):

        print("run_alert START")

        with open(Alert.PATH, "w") as f:
            # Telnetセッションを開始
            tn = Telnet(Alert.HOST, Alert.PORT)
            tn.read_until(b"login: ")
            tn.write(Alert.USER.encode("UTF-8") + b"\r\n")
            tn.read_until(b"password: ")
            tn.write(Alert.PASSWORD.encode("UTF-8") + b"\r\n")
            tn.read_until(b"QNET> ")
            
            while emergency_hosts:
                tn.write(Alert.ALERT_ON.encode("UTF-8") + b"\r\n")  # ALERT_ON
                time.sleep(2)  # 2秒待つ
                tn.write(Alert.ALERT_OFF.encode("UTF-8") + b"\r\n")  # ALERT_OFF
                for i in emergency_hosts:
                    print("emergency_get_status", emergency_hosts[i])
                    emergency = Sauna.get_status(emergency_hosts[i])
                    if not emergency:
                        del emergency_hosts[i]
                    print("emergency_hosts_running", emergency_hosts)
                    
            tn.read_until(b"QNET> ")
            # 結果を取得
            result = tn.read_until(b"QNET> ")
            # 結果をファイルに書き込む
            f.write(result.decode("UTF-8"))
            # Telnetセッションを終了
            tn.write(b"exit\r\n")

        print("run_alert END")

from telnetlib import Telnet
from create_path import CreatePath


class Sauna:

    HOST = "192.168.0.200"
    PORT = 23
    USER = "x1s"
    PASSWORD = "Admin12345"
    GET_STATUS = "?SYSVAR,4,1"
    PATH = CreatePath.create_path("get_status")


    def get_status(host):

        print("get_status START")

        emergency = False
        # テキストファイルを開く
        # with open(PATH, "w+", encoding="utf-8") as f:
        with open(Sauna.PATH, "w") as f:
            # Telnetセッションを開始
            tn = Telnet(host, Sauna.PORT, timeout=5)
            # tn = Telnet(host, PORT)
            tn.read_until(b"login: ")
            tn.write(Sauna.USER.encode("utf-8") + b"\r\n")
            tn.read_until(b"password: ")
            tn.write(Sauna.PASSWORD.encode("utf-8") + b"\r\n")
            tn.read_until(b"QNET> ")
            # コマンドを実行
            tn.write(Sauna.GET_STATUS.encode("utf-8") + b"\r\n")
            result = tn.read_until(b"QNET> ")
            # 結果をファイルに書き込む
            f.write(result.decode("utf-8"))
            # Telnetセッションを終了
            tn.write(b"exit\n")

        status = result.decode("utf-8").splitlines()[0].split(',')[3]
        print("status", status)

        if (status == '1'):
            emergency = True

        print("get_status END")

        return emergency

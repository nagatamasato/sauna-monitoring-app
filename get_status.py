from telnetlib import Telnet
from get_datetime import get_datetime


PORT = 23
USER = "x1s"
PASSWORD = "Admin12345"

GET_STATUS = "?SYSVAR,4,1"

DATETIME = get_datetime()
FILE_NAME = DATETIME + "_get-status.log"
PATH = ".\\logs\\get_status\\" + FILE_NAME


def get_status(host):

    print("get_status START")

    emergency = False
    # テキストファイルを開く
    # with open(PATH, "w+", encoding="utf-8") as f:
    with open(PATH, "w") as f:
        # Telnetセッションを開始
        tn = Telnet(host, PORT, timeout=5)
        # tn = Telnet(host, PORT)
        tn.read_until(b"login: ")
        tn.write(USER.encode("utf-8") + b"\r\n")
        tn.read_until(b"password: ")
        tn.write(PASSWORD.encode("utf-8") + b"\r\n")
        tn.read_until(b"QNET> ")
        # コマンドを実行
        tn.write(GET_STATUS.encode("utf-8") + b"\r\n")
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

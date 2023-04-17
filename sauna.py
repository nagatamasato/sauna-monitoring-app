from telnetlib import Telnet
from create_path import CreatePath
import json
import time

class Sauna:

    HOST = "192.168.0.200"
    PORT = 23
    USER = "x1s"
    PASSWORD = "Admin12345"
    GET_STATUS = "?SYSVAR,4,1"
    PATH = CreatePath.create_path("status")


    def get_status(hosts):

        print("get_status START")

        # open new file
        with open(Sauna.PATH, "w") as f:

            # header
            f.write("room ")
            f.write("host ")
            f.write("result\n")

            for i in hosts:
                f.write(i)
                f.write(" ")
                f.write(hosts[i])
                f.write(" ")
                # start Telnet session
                tn = Telnet(hosts[i], Sauna.PORT, timeout=5)
                # tn = Telnet(host, PORT)
                tn.read_until(b"login: ")
                tn.write(Sauna.USER.encode("utf-8") + b"\r\n")
                tn.read_until(b"password: ")
                tn.write(Sauna.PASSWORD.encode("utf-8") + b"\r\n")
                tn.read_until(b"QNET> ")
                # run command
                tn.write(Sauna.GET_STATUS.encode("utf-8") + b"\r\n")
                result = tn.read_until(b"QNET> ")
                result = result.decode("utf-8")
                result = result.replace("QNET> ", "")
                result = result.replace("\n", "")
                print("result-1", result)
                # write result
                f.write(result)

                status = result.splitlines()[0].split(',')[3]
                print("status", status)

                with open("statuses.json", "r") as jsonf:
                    statuses = json.load(jsonf)
                    print("statuses", statuses)
                    print("old_status", statuses[i]['status'])
                    print("new_status", status)
                    statuses[i]['status'] = status

                with open('statuses.json', 'w') as jsonf:
                    json.dump(statuses, jsonf)

                # terminate Telnet session
                tn.write(b"exit\n")
                time.sleep(1)

        print("get_status END")

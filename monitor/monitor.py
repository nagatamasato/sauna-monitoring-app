from telnetlib import Telnet
import datetime
import json
import time
import sys
sys.path.append('..\\common')
sys.path.append('..\\view')
from path import CreatePath
from view import View


class Monitor:

    HOST = "192.168.0.200"
    PORT = 23
    USER = "x1s"
    PASSWORD = "Admin12345"
    GET_STATUS = "?SYSVAR,4,1"
    PATH = CreatePath.create_path("monitor")


    def get_status(hosts):

        print("get_status START")

        # open new file
        with open(Monitor.PATH, "w") as f:

            # header
            f.write("room ")
            f.write("host ")
            f.write("result\n")

            for i in hosts:
                f.write(i)
                f.write(" ")
                f.write(hosts[i]['host'])
                f.write(" ")
                # start Telnet session
                tn = Telnet(hosts[i]['host'], Monitor.PORT, timeout=5)
                # tn = Telnet(host, PORT)
                tn.read_until(b"login: ")
                tn.write(Monitor.USER.encode("utf-8") + b"\r\n")
                tn.read_until(b"password: ")
                tn.write(Monitor.PASSWORD.encode("utf-8") + b"\r\n")
                tn.read_until(b"QNET> ")
                # run command
                tn.write(Monitor.GET_STATUS.encode("utf-8") + b"\r\n")
                result = tn.read_until(b"QNET> ")
                result = result.decode("utf-8")
                result = result.replace("QNET> ", "")
                result = result.replace("\n", "")
                print("result", result)
                # write result
                f.write(result)

                current_status = result.splitlines()[0].split(',')[3]
                print("status", current_status)

                now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                print("現在時刻は: ", now)

                with open("..\\hosts.json", "r") as jsonf:
                    hosts = json.load(jsonf)
                    print("statuses", hosts)
                    print("old_status", hosts[i]['status'])
                    print("new_status", current_status)
                    hosts[i]['status'] = current_status
                    hosts[i]['updated_time'] = now

                with open("..\\hosts.json", "w") as jsonf:
                    json.dump(hosts, jsonf)

                View.create_view(hosts)

                # terminate Telnet session
                tn.write(b"exit\n")
                time.sleep(1)

        print("get_status END")

from telnetlib import Telnet
from datetime import datetime
import json
import time
import sys
sys.path.append('..\\common')
sys.path.append('..\\view')
from log_manager import LogManager
from view import View


class Monitor:

    HOST = "192.168.0.200"
    PORT = 23
    USER = "x1s"
    PASSWORD = "Admin12345"
    GET_STATUS = "?SYSVAR,4,1"
    PATH = LogManager.create_path("monitor")


    def get_status(hosts):

        print("get_status START")

        with open(Monitor.PATH, "a") as f:
            header = "Room,Status,Updated_time,Host\n"
            f.write(header)
            # count = 0
            for i in hosts:
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

                current_status = result.splitlines()[0].split(',')[3]
                print("current_status", current_status)

                now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                print("現在時刻は: ", now)

                with open("..\\hosts.json", "r") as jsonf:
                    hosts = json.load(jsonf)
                    print("statuses", hosts)
                    print("old_status", hosts[i]['status'])
                    print("new_status", current_status)
                    hosts[i]['status'] = current_status
                    # if (count % 4 == 0):
                    #     hosts[i]['status'] = '1'
                    hosts[i]['updated_time'] = now

                with open("..\\hosts.json", "w") as jsonf:
                    json.dump(hosts, jsonf)

                log = i + "," + current_status + "," + now + "," + hosts[i]['host'] + "\n"
                f.write(log)

                View.create_view(hosts)

                # terminate Telnet session
                tn.write(b"exit\n")
                time.sleep(1)
                # count += 1

        print("get_status END")

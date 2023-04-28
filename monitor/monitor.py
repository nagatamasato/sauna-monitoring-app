from telnetlib import Telnet
from datetime import datetime
import os
import json
import time
import sys
sys.path.append('..\\common')
sys.path.append('..\\view')
from path_generator import PathGenerator
from generate_html import GenerateHtml


class Monitor:

    __APP_NAME = "monitor"
    __PORT = 23
    __USER = "x1s"
    __PASSWORD = "Admin12345"
    __GET_STATUS_COMMAND = "?SYSVAR,4,1"
    __PATH = PathGenerator.create_path(__APP_NAME)


    def get_status(hosts):

        print("get_status START")

        write_header = False

        if not os.path.exists(Monitor.__PATH):
            write_header = True

        with open(Monitor.__PATH, "a") as f:
            if write_header:
                header = "Room,Status,Emergency_time,Updated_time,Host\n"
                f.write(header)
                write_header = False
            for i in hosts:
                # start Telnet session
                tn = ""
                try:
                    tn = Telnet(hosts[i]['host'], Monitor.__PORT, timeout=5)
                    # tn = Telnet(host, PORT)
                    tn.read_until(b"login: ")
                    tn.write(Monitor.__USER.encode("utf-8") + b"\r\n")
                    tn.read_until(b"password: ")
                    tn.write(Monitor.__PASSWORD.encode("utf-8") + b"\r\n")
                    tn.read_until(b"QNET> ")
                    # run command
                    tn.write(Monitor.__GET_STATUS_COMMAND.encode("utf-8") + b"\r\n")
                    result = tn.read_until(b"QNET> ")
                    result = result.decode("utf-8")
                    result = result.replace("QNET> ", "")
                    result = result.replace("\n", "")
                    result = result.splitlines()[0].split(',')[3]

                except:
                    result = "Connection error"

                current_status = result
                print("current_status", current_status)

                now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                print("current time: ", now)
 
                with open("..\\hosts.json", "r") as jsonf:
                    hosts = json.load(jsonf)

                print("statuses", hosts)
                print("old_status", hosts[i]['status'])
                print("new_status", current_status)

                hosts[i]['status'] = current_status

                # 緊急ボタンONを最初に検知した時刻をセット
                if hosts[i]['status'] == '1' and hosts[i]['emergency_time'] == "":
                    hosts[i]['emergency_time'] = now
                # 緊急ボタンOFFを検知した場合は空欄に戻す
                if hosts[i]['status'] == '0':
                    hosts[i]['emergency_time'] = ""

                hosts[i]['updated_time'] = now

                with open("..\\hosts.json", "w") as jsonf:
                    json.dump(hosts, jsonf)

                emergency_time = hosts[i]['emergency_time']
                log = i + "," + current_status + "," + emergency_time + "," + now + "," + hosts[i]['host'] + "\n"
                f.write(log)

                GenerateHtml.generate_html(hosts)

                # terminate Telnet session
                if tn:
                    tn.write(b"exit\n")
                    time.sleep(1)
                # count += 1

        print("get_status END")

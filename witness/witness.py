import pymsteams
import json


class Witness:

    def __init__(self):
        # Webhook URL
        self.__TEAMS_URL = "https://x1studiocojp.webhook.office.com/webhookb2/2359c523-6ff7-4e43-9cce-b924c34b9a1b@3e594155-a0af-40ef-a8f2-dc8ce23f3844/IncomingWebhook/5798f01fbb53408ea38a9651139d18ea/4eb77287-1789-4810-b206-e1c3bd304107"

        self.__HOSTS_FILES = [
            "..\\hosts_1.json",
            "..\\hosts_2.json",
            "..\\hosts_3.json"
        ]


    def report(self):

        message = "Hi, Sauna Emergency App is working fine."
        connection_errors = ""

        for i in range(len(self.__HOSTS_FILES)):
            with open(self.__HOSTS_FILES[i], "r") as f:
                hosts = json.load(f)

            for key in hosts:
                if hosts[key]['status'] == "Connection Error":
                    message = "Hi, I got a Connection Error in the next sauna room.<br>"
                    connection_errors += key + "<br>"

        print("connection_errors", connection_errors)
        message += connection_errors
        myTeamsMessage = pymsteams.connectorcard(self.__TEAMS_URL)
        myTeamsMessage.title("Witness Report")
        myTeamsMessage.text(message)
        myTeamsMessage.send()

import json
from alert import Alert


with open("statuses.json", "r") as f:
    statuses = json.load(f)

print("statuses", statuses)

emergencies = {}
for i in statuses:
    if statuses[i]['status'] == "1":
        emergencies[i] = statuses[i]

print("emergencies", emergencies) 

if (emergencies):
    Alert.alert()

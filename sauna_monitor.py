from get_status import get_status
from run_alert import run_alert
import time

hosts = {
    "101": "192.168.0.200",
    # "102": "192.168.0.201",
    # "103": "192.168.0.202",
    # "201": "192.168.0.203",
    # "207": "192.168.0.209",
    # "301": "192.168.0.210",
    # "307": "192.168.0.216",
    # "401": "192.168.0.217",
    # "407": "192.168.0.223",
    # "501": "192.168.0.224",
    # "507": "192.168.0.230"
}

emergency_hosts = {}

for i in hosts:
    print("get_status", i, hosts[i])
    emergency = get_status(hosts[i])
    if emergency:
        emergency_hosts[i] = hosts[i]
    time.sleep(1)

print("emergency_hosts", emergency_hosts)

if (emergency_hosts):
    run_alert(emergency_hosts)

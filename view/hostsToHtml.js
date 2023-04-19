const hosts = {
    "101": {
        "host": "192.168.0.200",
        "status": "0"
    },
    "102": {
        "host": "192.168.0.201",
        "status": "0"
    },
    "103": {
        "host": "192.168.0.202",
        "status": "0"
    },
    "201": {
        "host": "192.168.0.203",
        "status": "0"
    },
    "207": {
        "host": "192.168.0.209",
        "status": "0"
    },
    "301": {
        "host": "192.168.0.210",
        "status": "0"
    },
    "307": {
        "host": "192.168.0.216",
        "status": "0"
    },
    "401": {
        "host": "192.168.0.217",
        "status": "0"
    },
    "407": {
        "host": "192.168.0.223",
        "status": "0"
    },
    "501": {
        "host": "192.168.0.224",
        "status": "0"
    },
    "507": {
        "host": "192.168.0.230",
        "status": "0"
    }
};

let html = '';
for (const key in hosts) {
    const host = hosts[key];
    const row = `<tr><td>${key}</td><td>${host.status}</td><td>${host.host}</td></tr>`;
    html += row;
}

const table = document.getElementById('hosts');
table.innerHTML = html;
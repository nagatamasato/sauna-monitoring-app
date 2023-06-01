import json


class GenerateHtml:

    def __init__(self):

        self.__hosts_files = [
            "..\\hosts_1.json",
            "..\\hosts_2.json",
            "..\\hosts_3.json"
        ]


    def monitoring(self):

        # Generate HTML
        html = "<!DOCTYPE html>\n"
        html += "<html>\n"
        html += "<head>\n"
        html += '   <link rel="stylesheet" type="text/css" href="css/styles.css">\n'
        html += "   <title>Sauna rooms monitoring</title>\n"
        html += "</head>\n"
        html += "<body>\n"
        html += "   <h1>Sauna rooms monitoring</h1>\n"
        html += '   <div class="button-wrapper">\n'
        html += "       <button onclick="
        html += "location.href='history.html'\n"
        html += '           class="btn-square">\n'
        html += "           History\n"
        html += "       </button>\n"
        html += "   </div>\n"
        html += "   <table>\n"
        html += "       <thead>\n"
        html += "           <tr><th>Room</th><th>Status</th><th>Last emergency</th><th>Updated time</th><th>Host</th></tr>\n"
        html += "       </thead>\n"
        html += '       <tbody id="hosts">\n'

        hosts_files = self.__hosts_files
        for i in range(len(hosts_files)):
            with open(hosts_files[i], "r") as jsonf:
                hosts = json.load(jsonf)
            # Parses JSON data and adds each row of data to a table
            for room in hosts:
                host = hosts[room]['host']
                status = hosts[room]['status']
                if hosts[room]['status'] == '1':
                    status = "Emergency"
                elif hosts[room]['status'] == '0':
                    status = "Normal"
                last_emergency = ""
                if hosts[room]['history']:
                    last_emergency = hosts[room]['history'][-1]
                updated_time = hosts[room]['updated_time']
                html += f"           <tr><td>{room}</td><td>{status}</td><td>{last_emergency}</td><td>{updated_time}</td><td>{host}</td></tr>\n"
            
        html += "       </tbody>\n"
        html += "   </table>\n"
        html += '<script src="js/index.js"></script>\n'
        html += "</body>\n"
        html += "</html>"

        # Export HTML to file
        with open('..\\view\\index.html', 'w') as f:
            f.write(html)


    def history(self):

        # Generate HTML
        html = "<!DOCTYPE html>\n"
        html += "<html>\n"
        html += "<head>\n"
        html += '   <link rel="stylesheet" type="text/css" href="css/styles.css">\n'
        html += "   <title>History of the last three</title>\n"
        html += "</head>\n"
        html += "<body>\n"
        html += "   <h1>History of the last three</h1>\n"
        html += '   <div class="button-wrapper">\n'
        html += "       <button onclick="
        html += "location.href='index.html'\n"
        html += '           class="btn-square">\n'
        html += "           Monitoring\n"
        html += "       </button>\n"
        html += "   </div>\n"

        # Create table headers
        table_header = '    <tr><th>Room</th><th>Emergency date</th></tr>\n'

        hosts_files = self.__hosts_files
        table_rows = ''
        for i in range(len(hosts_files)):
            with open(hosts_files[i], "r") as jsonf:
                hosts = json.load(jsonf)
            # Create each row of the table
            for room in hosts:
                # Sort by date in descending order
                history = sorted(hosts[room]['history'], reverse=True)
                # Create table rows
                row = '     <tr><td>{}</td><td>{}</td></tr>\n'.format(room, '</td></tr><tr><td></td><td>'.join(history))
                # Add a table row
                table_rows += row

        # Create table
        table = '   <table>\n{} </table>\n'.format(table_header + table_rows)
        html += table
        html += '<script src="js/history.js"></script>\n'
        html += "</body>\n"
        html += "</html>"
        # Export HTML to file
        with open('..\\view\\history.html', 'w') as f:
            f.write(html)

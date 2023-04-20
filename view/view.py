class View:

    def create_view(hosts):

        # hosts = {
        #     "101": {
        #         "host": "192.168.0.200",
        #         "status": "0",
        #         "updated_time": ""
        #     },
        #     "102": {
        #         "host": "192.168.0.201",
        #         "status": "0",
        #         "updated_time": ""
        #     },
        #     "103": {
        #         "host": "192.168.0.202",
        #         "status": "0",
        #         "updated_time": ""
        #     },
        #     "201": {
        #         "host": "192.168.0.203",
        #         "status": "0",
        #         "updated_time": ""
        #     },
        #     "207": {
        #         "host": "192.168.0.209",
        #         "status": "0",
        #         "updated_time": ""
        #     },
        #     "301": {
        #         "host": "192.168.0.210",
        #         "status": "0",
        #         "updated_time": ""
        #     },
        #     "307": {
        #         "host": "192.168.0.216",
        #         "status": "0",
        #         "updated_time": ""
        #     },
        #     "401": {
        #         "host": "192.168.0.217",
        #         "status": "0",
        #         "updated_time": ""
        #     },
        #     "407": {
        #         "host": "192.168.0.223",
        #         "status": "0",
        #         "updated_time": ""
        #     },
        #     "501": {
        #         "host": "192.168.0.224",
        #         "status": "0",
        #         "updated_time": ""
        #     },
        #     "507": {
        #         "host": "192.168.0.230",
        #         "status": "0",
        #         "updated_time": ""
        #     }
        # }
        print("hosts in view.py", hosts)

        # HTMLのテーブルを作成する
        html = "<!DOCTYPE html>\n"
        html += "<html>\n"
        html += "<head>\n"
        html += '<link rel="stylesheet" type="text/css" href="styles.css">\n'
        html += "<title>Sauna rooms monitoring</title>\n"
        html += "</head>\n"
        html += "<body>\n"
        html += "<h1>Sauna rooms monitoring</h1>"
        html += "<table>\n"
        html += "<thead>\n"
        html += "<tr><th>Room</th><th>Status</th><th>Updated time</th><th>Host</th></tr>\n"
        html += "</thead>\n"
        html += '<tbody id="hosts">\n'

        # JSONデータを解析し、各行のデータをテーブルに追加する
        for room, info in hosts.items():
            host = info['host']
            status = info['status']
            updated_time = info['updated_time']
            html += f"<tr><td>{room}</td><td>{status}</td><td>{updated_time}</td><td>{host}</td></tr>\n"
        
        html += "</tbody>\n"
        html += "</table>"
        html += '<script src="view.js"></script>\n'
        html += "</body>\n"

        # HTMLのテーブルをファイルに書き出す
        with open('..\\view\\index.html', 'w') as f:
            f.write(html)

        # headers = []
        # rows = []
        # for i in hosts:
        #     # 最初の要素をヘッダーとして取得
        #     if not headers:
        #         headers = list(i)
                
        #     # 各行のデータを取得
        #     # rows.append(list(i.values()))

        #     print("headers", headers)
        #     # print("rows", rows)

        # # headers = list(hosts[0].keys())
        # # rows = [list(i.values()) for i in hosts]
        
        # template = """
        # <!DOCTYPE html>
        # <html>
        # <head>
        #     <link rel="stylesheet" type="text/css" href="styles.css">
        #     <title>Sauna room's statuses</title>
        # </head>
        # <body>
        #     <table>
        #         <thead>
        #             <tr>
        #                 <th>Room</th>
        #                 <th>Status</th>
        #                 <th>Host</th>
        #             </tr>
        #         </thead>
        #         <tbody id="hosts">
        #         </tbody>
        #     </table>
        #     <script src="hostsView.js"></script>
        # </body>
        # </html>
        # """
        # print("template", template)

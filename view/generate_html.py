class GenerateHtml:

    def generate_html(hosts):

        print("hosts in generate_html.py", hosts)

        # HTMLのテーブルを作成する
        html = "<!DOCTYPE html>\n"
        html += "<html>\n"
        html += "<head>\n"
        html += '   <link rel="stylesheet" type="text/css" href="styles.css">\n'
        html += "   <title>Sauna rooms monitoring</title>\n"
        html += "</head>\n"
        html += "<body>\n"
        html += "   <h1>Sauna rooms monitoring</h1>\n"
        html += "   <table>\n"
        html += "       <thead>\n"
        html += "           <tr><th>Room</th><th>Status</th><th>Emergency time</th><th>Updated time</th><th>Host</th></tr>\n"
        html += "       </thead>\n"
        html += '       <tbody id="hosts">\n'

        # JSONデータを解析し、各行のデータをテーブルに追加する
        for room, info in hosts.items():
            host = info['host']
            status = info['status']
            if info['status'] == '1':
                status = "Emergency"
            elif info['status'] == '0':
                status = "Normal"
            emergency_time = info['emergency_time']
            updated_time = info['updated_time']
            html += f"           <tr><td>{room}</td><td>{status}</td><td>{emergency_time}</td><td>{updated_time}</td><td>{host}</td></tr>\n"
        
        html += "       </tbody>\n"
        html += "   </table>\n"
        html += '<script src="main.js"></script>\n'
        html += "</body>\n"
        html += "</html>\n"

        # HTMLのテーブルをファイルに書き出す
        with open('..\\view\\index.html', 'w') as f:
            f.write(html)

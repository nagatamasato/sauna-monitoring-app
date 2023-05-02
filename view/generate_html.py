import json


class GenerateHtml:

    def monitoring():

        with open("..\\hosts.json", "r") as jsonf:
            hosts = json.load(jsonf)
        # HTML作成
        html = "<!DOCTYPE html>\n"
        html += "<html>\n"
        html += "<head>\n"
        html += '   <link rel="stylesheet" type="text/css" href="css/styles.css">\n'
        html += "   <title>Sauna rooms monitoring</title>\n"
        html += "</head>\n"
        html += "<body>\n"
        html += "   <h1>Sauna rooms monitoring</h1>\n"
        html += '   <div calss="button-wrapper">\n'
        html += "       <button onclick="
        html += "location.href='history.html'\n"
        html += '           class="btn-square">\n'
        html += "           History\n"
        html += "       </button>\n"
        html += "   </div>\n"
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
        html += '<script src="js/index.js"></script>\n'
        html += "</body>\n"
        html += "</html>"

        # HTMLをファイルに書き出す
        with open('..\\view\\index.html', 'w') as f:
            f.write(html)


    def history():

        with open("..\\allHosts.json", "r") as jsonf:
            hosts = json.load(jsonf)
        # HTML生成
        html = "<!DOCTYPE html>\n"
        html += "<html>\n"
        html += "<head>\n"
        html += '   <link rel="stylesheet" type="text/css" href="css/styles.css">\n'
        html += "   <title>Emergency history</title>\n"
        html += "</head>\n"
        html += "<body>\n"
        html += "   <h1>Emergency history</h1>\n"
        html += '   <div class="button-wrapper">\n'
        html += "       <button onclick="
        html += "location.href='index.html'\n"
        html += '           class="btn-square">\n'
        html += "           Monitoring\n"
        html += "       </button>\n"
        html += "   </div>\n"

        # テーブルのヘッダーを作成
        table_header = '    <tr><th>Room</th><th>Emergency date</th></tr>\n'

        # テーブルの各行を作成
        table_rows = ''
        for room, history in hosts.items():
            # 日付の降順にソート
            history = sorted(history['history'], reverse=True)
            # テーブルの行を作成
            row = '     <tr><td>{}</td><td>{}</td></tr>\n'.format(room, '</td></tr><tr><td></td><td>'.join(history))
            # テーブルの行を追加
            table_rows += row
        # テーブルを作成する
        table = '   <table>\n{} </table>\n'.format(table_header + table_rows)
        html += table
        html += '<script src="js/history.js"></script>\n'
        html += "</body>\n"
        html += "</html>"
        # HTMLをファイルに書き出す
        with open('..\\view\\history.html', 'w') as f:
            f.write(html)

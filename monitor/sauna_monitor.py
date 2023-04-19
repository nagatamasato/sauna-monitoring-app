from datetime import datetime
import time
import json

from monitor import Monitor


# 定期実行間隔
INTERVAL = 60
# 1回のINTERVAL中の実行回数
FREQUENCY = 6
# 余裕を持たせるための時間(これがないと実行時間がINTERVAL(60秒)を超える)
MARGIN = 0.5
# １回あたりの最大時間
MAXTIME = (INTERVAL / FREQUENCY) - MARGIN
# MAXTIME = (INTERVAL / FREQUENCY)

start_time = datetime.now()
print("start_time", start_time)

with open("..\\hosts.json", "r") as f:
    hosts = json.load(f)

for i in range(FREQUENCY):
    print(i + 1, "/", FREQUENCY)
    # 開始時刻
    start = datetime.now()
    # サウナルームのステータスを取得
    Monitor.get_status(hosts)
    # 終了時刻
    end = datetime.now()
    # 実行時間
    runtime = (end - start).total_seconds()

    print("start", start)
    print("end", end)
    print("runtime", runtime)

    wait = MAXTIME - runtime
    print("wait", wait)
    if (wait > 0):
        time.sleep(wait)

    end_time = datetime.now()
    total_time = (end_time - start_time).total_seconds()
    print("end_time", end_time)
    print("total_time", total_time)

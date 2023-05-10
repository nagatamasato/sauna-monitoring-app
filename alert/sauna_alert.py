from datetime import datetime
import time
from alert import Alert


# 定期実行間隔
INTERVAL = 60
# 1回のINTERVAL中の実行回数
FREQUENCY = 30
# 余裕を持たせるための時間(これがないと実行時間がINTERVAL(60秒)を超える)
MARGIN = 0.5
# １回あたりの最大時間
MAXTIME = (INTERVAL / FREQUENCY) - MARGIN

if (MAXTIME < 0):
    MARGIN = 0

start_time = datetime.now()
print("start_time", start_time)

alert = Alert()

for i in range(FREQUENCY):
    print(i + 1, "/", FREQUENCY)
    # 開始時刻
    start = datetime.now()

    json_files = [
        "..\\hosts_1.json",
        "..\\hosts_2.json",
        "..\\hosts_3.json"
    ]

    for j in range(len(json_files)):
        alert.check_emergency(json_files[j])

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

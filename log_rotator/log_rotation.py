from datetime import datetime
from rotator import Rotator


start_time = datetime.now()
print("rotation_START_time", start_time)

Rotator.rotate_monitor_log()
Rotator.rotate_alert_log()
Rotator.rotate_log_rotator_log()

end_time = datetime.now()
print("rotation_END_time", end_time)

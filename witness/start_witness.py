from witness import Witness

witness = Witness()

# check monitor
# witness.monitor_1_check()

# check alert
witness.alert()

# check log rotation
witness.log_rotation('monitor')
witness.log_rotation('alert')

# check connection error
witness.sauna_current_connection()

# send report
witness.report()

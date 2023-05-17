from witness import Witness

witness = Witness()

# check monitor
witness.monitor_1_check()

# check log rotation
witness.log_rotation_check('monitor')
witness.log_rotation_check('alert')

# check connection error
witness.connection_check()

# send report
witness.report()

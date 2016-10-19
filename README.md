# SerialLog
Dead Simple Serial Logger in Python.

Simple script to log data coming from a serial port. The logfile rotates at
midnight.

# Arguments
-p is not optional.

	optional arguments:
	  -h, --help  show this help message and exit
		-p P        PORT - Full path to port. Ex. '-p /dev/ttyUSB0'
		-b B        BAUD rate. Ex. '-b 9600'
		-n N        NEWLINE character (ascii hex) (default is 0x0D (cr)). Ex. '-d
		            0A'
		-f F        Name of the log FILE. If absent, the port name will be used.

# Examples:

	'python SerialLogger.py -p /dev/ttyUSB0 -b 19200'
	'python SerialLogger.py -p /dev/ttyUSB0 -n cr'
	'python SerialLogger.py -p /dev/ttyUSB0 -b 19200 -n lf -f ard_out.log'
	'nohup python SerialLogger.py -p /dev/ttyUSB0 -b 19200 &'

from __future__ import print_function
import argparse, serial, io, time, logging
from logging import handlers

""" Dead Simple Serial Logger """
""" TODO:
      - hwgrep port specification
      - Windows support & testing
      - newLine transformations (cr -> crlf, lf -> crlf)
      - Proper documentation
"""

_addr = ''
_baud = 9600
_newline = '\x0A'
_logName = ''

# Parse Args
parser = argparse.ArgumentParser(description='Simple script to log data coming from a serial port. The logfile rotates at midnight.')
parser.add_argument('-p', help="PORT - Full path to port. Ex. '-p /dev/ttyUSB0'")
parser.add_argument('-b', help="BAUD rate. Ex. '-b 9600'")
parser.add_argument('-n', help="NEWLINE character (ascii hex) (default is 0x0D (cr)). Ex. '-d 0A'")
parser.add_argument('-f', help="Name of the log FILE. If absent, the port name will be used.")
args = parser.parse_args()

if args.p:
	if args.p.endswith('/'):
		print("Warning: Removing the port's trailing slash for you...")
		_addr = args.p[:-1]
	else:
		_addr = args.p
else:
	print("A port must be specified.")
	parser.print_help()
	exit(0)

if args.b:
	_baud = int(args.b)

if args.n:
	if args.n is 'cr':
		_newline = '\x0D'
	if args.n is 'lf' or args.n is 'crlf':
		_newline = '\x0A'
	else:
		_newline = args.n.decode("hex")

if args.f:
	_logName = args.f
else:
	_logName = _addr.split('/')[-1] + '.log'


# Logging. Note the 2 handlers: console and file. Console is more verbose than file.
logger = logging.getLogger('serialLogger')
logger.setLevel(logging.DEBUG)
fh = handlers.TimedRotatingFileHandler(_logName, when='midnight')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch_formatter = logging.Formatter('%(asctime)s [%(name)s][%(levelname)s] %(message)s')
fh_formatter = logging.Formatter('%(asctime)s: %(message)s')
fh.setFormatter(fh_formatter)
ch.setFormatter(ch_formatter)
logger.addHandler(fh)
logger.addHandler(ch)

logger.info("Serial Logger Started.")
logger.info("PORT: %s" % _addr)
logger.info("BAUD: %s" % _baud)
logger.info("NEWLINE: %s" % _newline.encode("hex"))
logger.info("LOGFILE: %s\n" % _logName)

try:
	with serial.Serial(_addr,_baud) as pt:
	    spb = io.TextIOWrapper(io.BufferedRWPair(pt,pt,1),
	        encoding='ascii', errors='ignore', newline=_newline,line_buffering=True)
	    spb.readline()  # throw away first line; likely to start mid-sentence (incomplete)
	    while (1):
	        x = spb.readline()  # read one line of text from serial port
	        if '\x0A' in _newline:
	        	x = x[:-1] # Get rid of the extra linefeed, since logger will add its own
	        logger.info(x)
except KeyboardInterrupt:
	logger.info("Serial Logger Stopping.")
	print("Goodbye...")
	exit(0)

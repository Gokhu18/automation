import logging
logger = logging.getLogger('program')
# create file handler which logs even debug messages
hdlr = logging.FileHandler('samilo.log')
hdlr.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

def log_error(val):
	# error files will be printed since are greater than warnings
	logger.error(val)

def log_info(val):
	logger.info(val)
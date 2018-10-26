import logging
logger = logging.getLogger('program')
hdlr = logging.FileHandler('samilo.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(20)

def log_error(val):
	# error files will be printed since are greater than warnings
	logger.error(val)

def log_info(val):
	logger.info(val)
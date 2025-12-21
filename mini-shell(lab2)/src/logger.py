import logging
import os

def setup_logging(log_file='shell.log'):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='[%(asctime)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def log_cmd(cmd, error=None):
    if error:
        logging.error(f"{cmd} | ERROR: {error}")
    else:
        logging.info(cmd)

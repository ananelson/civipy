import logging
import os


# load credentials from OS environment
REST_BASE = os.environ['CIVI_REST_BASE']
USER_KEY = os.environ['CIVI_USER_KEY']
SITE_KEY = os.environ['CIVI_SITE_KEY']


# set up logging
logger = logging.getLogger("civipy")
logger.setLevel(logging.DEBUG)

LOG_FILE = os.environ.get("CIVIPY_LOG_FILE")
if LOG_FILE:
    h = logging.FileHandler(LOG_FILE)
    h.setLevel(logging.DEBUG)
    logger.addHandler(h)

logger.warning("civipy is logging to here!")

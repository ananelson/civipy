import logging
import os


# load credentials from OS environment
REST_BASE = os.environ.get('CIVI_API_BASE') or os.environ.get("CIVI_REST_BASE")

if 'http' in REST_BASE:
    API_TYPE = 'http'
elif 'drush' in REST_BASE:
    API_TYPE = 'drush'
else:
    API_TYPE = 'cvcli'

USER_KEY = os.environ.get('CIVI_USER_KEY')
SITE_KEY = os.environ.get('CIVI_SITE_KEY')

# set up logging
logger = logging.getLogger("civipy")
logger.setLevel(logging.DEBUG)

LOG_FILE = os.environ.get("CIVIPY_LOG_FILE")
if LOG_FILE:
    h = logging.FileHandler(LOG_FILE)
    h.setLevel(logging.DEBUG)
    logger.addHandler(h)

logger.warning("civipy is logging to here!")

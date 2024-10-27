import logging

# Configure logging
logging.basicConfig(
    filename='error_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger()

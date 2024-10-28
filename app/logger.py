import os
import logging

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    filename='logs/error_log.log',
    level=logging.ERROR,  # Change to ERROR to log error messages
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger()

# Example of logging an error message
logger.error("This is an error message.")

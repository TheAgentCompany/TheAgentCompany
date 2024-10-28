import logging
import sys

def setup_logging(level=logging.INFO):
    """Configure logging for the entire application."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('application.log')
        ]
    )
    
    # Create a logger instance that will be used across the application
    logger = logging.getLogger('openhands')
    return logger

# Create a default logger instance
logger = setup_logging()

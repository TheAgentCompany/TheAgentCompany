import logging
import sys
import os

def setup_logging(level=logging.INFO, log_file='application.log'):
    """Configure logging for the entire application."""
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_file)

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_path)
        ]
    )
    
    # Create a logger instance that will be used across the application
    logger = logging.getLogger('openhands')
    return logger

# Create a default logger instance
logger = setup_logging()

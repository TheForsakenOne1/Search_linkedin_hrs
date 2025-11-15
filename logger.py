"""
Logging utilities for LinkedIn scraper
Provides structured logging with different levels
"""
import logging
import os
from datetime import datetime
import sys


class ScraperLogger:
    """Custom logger for LinkedIn scraper with file and console output"""

    def __init__(self, name='linkedin_scraper', log_dir='logs', level=logging.INFO):
        """
        Initialize logger

        Args:
            name (str): Logger name
            log_dir (str): Directory for log files
            level (int): Logging level
        """
        self.name = name
        self.log_dir = log_dir
        self.level = level

        # Create logs directory
        os.makedirs(log_dir, exist_ok=True)

        # Setup logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Remove existing handlers
        self.logger.handlers = []

        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        simple_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )

        # File handler (detailed)
        log_file = os.path.join(
            log_dir,
            f'{name}_{datetime.now().strftime("%Y%m%d")}.log'
        )
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(file_handler)

        # Console handler (simple)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(simple_formatter)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)

    def info(self, message):
        """Log info message"""
        self.logger.info(message)

    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)

    def error(self, message, exc_info=False):
        """Log error message"""
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message, exc_info=False):
        """Log critical message"""
        self.logger.critical(message, exc_info=exc_info)

    def log_scraping_start(self, company, max_results):
        """Log start of scraping"""
        self.info(f"Starting scraping campaign for {company} (max: {max_results} results)")

    def log_scraping_complete(self, company, results_count):
        """Log completion of scraping"""
        self.info(f"Scraping complete for {company}: {results_count} profiles found")

    def log_message_generation(self, count, ai_powered=False):
        """Log message generation"""
        method = "AI-powered" if ai_powered else "Template-based"
        self.info(f"Generating {count} messages using {method} generation")

    def log_export(self, file_path, format_type):
        """Log export operation"""
        self.info(f"Exported data to {format_type.upper()}: {file_path}")

    def log_error_with_context(self, error, context):
        """Log error with additional context"""
        self.error(f"{context}: {str(error)}", exc_info=True)

    def log_campaign_summary(self, campaign_id, stats):
        """Log campaign summary"""
        self.info(f"Campaign {campaign_id} summary: {stats}")


# Global logger instances
_loggers = {}


def get_logger(name='linkedin_scraper', level=logging.INFO):
    """
    Get or create a logger instance

    Args:
        name (str): Logger name
        level (int): Logging level

    Returns:
        ScraperLogger: Logger instance
    """
    if name not in _loggers:
        _loggers[name] = ScraperLogger(name, level=level)
    return _loggers[name]


def setup_logging(verbose=False):
    """
    Setup logging for the application

    Args:
        verbose (bool): Enable verbose logging (DEBUG level)

    Returns:
        ScraperLogger: Configured logger
    """
    level = logging.DEBUG if verbose else logging.INFO
    return get_logger(level=level)


# Convenience functions
def log_info(message, logger_name='linkedin_scraper'):
    """Log info message"""
    get_logger(logger_name).info(message)


def log_error(message, logger_name='linkedin_scraper', exc_info=False):
    """Log error message"""
    get_logger(logger_name).error(message, exc_info=exc_info)


def log_warning(message, logger_name='linkedin_scraper'):
    """Log warning message"""
    get_logger(logger_name).warning(message)


def log_debug(message, logger_name='linkedin_scraper'):
    """Log debug message"""
    get_logger(logger_name).debug(message)


if __name__ == "__main__":
    """Test logging"""
    print("Testing logging system...\n")

    # Create logger
    logger = setup_logging(verbose=True)

    # Test different log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    # Test specialized logging
    logger.log_scraping_start("Google", 50)
    logger.log_message_generation(10, ai_powered=True)
    logger.log_export("/path/to/file.csv", "csv")
    logger.log_scraping_complete("Google", 45)

    print("\n✓ Logging test complete. Check logs/ directory for log files.")

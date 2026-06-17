import logging
import os
from datetime import datetime


class ExceptionHandler:

    LOG_FOLDER = "logs"
    LOG_FILE = os.path.join(LOG_FOLDER, "error.log")

    @staticmethod
    def setup_logger():
        if not os.path.exists(ExceptionHandler.LOG_FOLDER):
            os.makedirs(ExceptionHandler.LOG_FOLDER)

        logging.basicConfig(
            filename=ExceptionHandler.LOG_FILE,
            level=logging.ERROR,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    @staticmethod
    def log_error(error_type, error, context=""):
        ExceptionHandler.setup_logger()

        logging.error(
            f"[{error_type}] {context} | {type(error).__name__}: {str(error)}"
        )

    @staticmethod
    def handle_api_error(error, context="API operation failed"):
        ExceptionHandler.log_error("API ERROR", error, context)

    @staticmethod
    def handle_file_error(error, context="File operation failed"):
        ExceptionHandler.log_error("FILE ERROR", error, context)

    @staticmethod
    def handle_data_error(error, context="Data parsing failed"):
        ExceptionHandler.log_error("DATA ERROR", error, context)

    @staticmethod
    def handle_input_error(error, context="Invalid user input"):
        ExceptionHandler.log_error("INPUT ERROR", error, context)

    @staticmethod
    def handle_chart_error(error, context="Chart generation failed"):
        ExceptionHandler.log_error("CHART ERROR", error, context)

    @staticmethod
    def handle_general_error(error, context="Unexpected error"):
        ExceptionHandler.log_error("GENERAL ERROR", error, context)
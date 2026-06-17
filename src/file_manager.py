import csv
import os
from datetime import datetime

from utils.exception_handler import ExceptionHandler


class FileManager:

    def __init__(self):
        self.file_path = "../data/weather_history.csv"
        self.ensure_history_file_exists()

    def ensure_history_file_exists(self):
        try:
            folder_path = os.path.dirname(self.file_path)

            if folder_path and not os.path.exists(folder_path):
                os.makedirs(folder_path)

            if not os.path.exists(self.file_path):
                with open(self.file_path, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Date", "City", "Temperature"])

        except OSError as e:
            ExceptionHandler.handle_file_error(
                e,
                "Creating weather history file"
            )

    def save_weather_data(self, weather_data):
        try:
            with open(self.file_path, "a", newline="") as file:
                writer = csv.writer(file)

                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    weather_data["city"],
                    weather_data["temperature"]
                ])

        except KeyError as e:
            ExceptionHandler.handle_data_error(
                e,
                "Missing weather data field while saving history"
            )

        except PermissionError as e:
            ExceptionHandler.handle_file_error(
                e,
                "Permission denied while saving weather history"
            )

        except OSError as e:
            ExceptionHandler.handle_file_error(
                e,
                "OS error while saving weather history"
            )

        except Exception as e:
            ExceptionHandler.handle_general_error(
                e,
                "Unexpected error while saving weather history"
            )

    def load_weather_history(self):
        history = []

        try:
            with open(self.file_path, "r") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    if "Date" in row and "City" in row and "Temperature" in row:
                        history.append(row)

            return history

        except FileNotFoundError as e:
            ExceptionHandler.handle_file_error(
                e,
                "Weather history file not found"
            )
            return []

        except PermissionError as e:
            ExceptionHandler.handle_file_error(
                e,
                "Permission denied while reading weather history"
            )
            return []

        except csv.Error as e:
            ExceptionHandler.handle_data_error(
                e,
                "Invalid CSV format in weather history file"
            )
            return []

        except OSError as e:
            ExceptionHandler.handle_file_error(
                e,
                "OS error while reading weather history"
            )
            return []

        except Exception as e:
            ExceptionHandler.handle_general_error(
                e,
                "Unexpected error while loading weather history"
            )
            return []
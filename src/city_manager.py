import json
import os

from utils.exception_handler import ExceptionHandler


class CityManager:

    def __init__(self):
        self.file_path = "../data/favorites.json"
        self.ensure_data_file_exists()

    def ensure_data_file_exists(self):
        try:
            folder_path = os.path.dirname(self.file_path)

            if folder_path and not os.path.exists(folder_path):
                os.makedirs(folder_path)

            if not os.path.exists(self.file_path):
                with open(self.file_path, "w") as file:
                    json.dump({"favorites": []}, file, indent=4)

        except OSError as e:
            ExceptionHandler.handle_file_error(
                e,
                "Creating favorites data file"
            )

    def load_favorites(self):
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                return data.get("favorites", [])

        except FileNotFoundError as e:
            ExceptionHandler.handle_file_error(
                e,
                "Favorites file not found"
            )
            return []

        except json.JSONDecodeError as e:
            ExceptionHandler.handle_data_error(
                e,
                "Invalid JSON format in favorites file"
            )
            return []

        except PermissionError as e:
            ExceptionHandler.handle_file_error(
                e,
                "Permission denied while reading favorites file"
            )
            return []

        except OSError as e:
            ExceptionHandler.handle_file_error(
                e,
                "OS error while reading favorites file"
            )
            return []

        except Exception as e:
            ExceptionHandler.handle_general_error(
                e,
                "Unexpected error while loading favorites"
            )
            return []

    def save_favorite_city(self, city):
        try:
            favorites = self.load_favorites()

            if city not in favorites:
                favorites.append(city)

                with open(self.file_path, "w") as file:
                    json.dump(
                        {"favorites": favorites},
                        file,
                        indent=4
                    )

        except PermissionError as e:
            ExceptionHandler.handle_file_error(
                e,
                f"Permission denied while saving favorite city: {city}"
            )

        except OSError as e:
            ExceptionHandler.handle_file_error(
                e,
                f"OS error while saving favorite city: {city}"
            )

        except Exception as e:
            ExceptionHandler.handle_general_error(
                e,
                f"Unexpected error while saving favorite city: {city}"
            )

    def remove_favorite_city(self, city):
        try:
            favorites = self.load_favorites()

            if city in favorites:
                favorites.remove(city)

                with open(self.file_path, "w") as file:
                    json.dump(
                        {"favorites": favorites},
                        file,
                        indent=4
                    )

        except PermissionError as e:
            ExceptionHandler.handle_file_error(
                e,
                f"Permission denied while removing favorite city: {city}"
            )

        except OSError as e:
            ExceptionHandler.handle_file_error(
                e,
                f"OS error while removing favorite city: {city}"
            )

        except Exception as e:
            ExceptionHandler.handle_general_error(
                e,
                f"Unexpected error while removing favorite city: {city}"
            )

    def show_favorites(self):
        favorites = self.load_favorites()

        if favorites:
            print("\nFavorite Cities:")

            for city in favorites:
                print("-", city)

        else:
            print("\nNo favorite cities saved yet.")
import os
import requests

from dotenv import load_dotenv
from utils.exception_handler import ExceptionHandler

load_dotenv()


class WeatherService:

    def __init__(self):
        self.api_key = os.getenv("API_KEY")

        if not self.api_key:
            error = ValueError("API_KEY not found in .env file")
            ExceptionHandler.handle_api_error(
                error,
                "Loading OpenWeatherMap API key"
            )
            raise error

        self.current_weather_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

    def get_weather(self, city):

        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            response = requests.get(
                self.current_weather_url,
                params=params,
                timeout=10
            )

            response.raise_for_status()
            data = response.json()

            weather_info = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "condition": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"]
            }

            return weather_info

        except requests.exceptions.ConnectionError as e:
            ExceptionHandler.handle_api_error(
                e,
                f"Connection error while fetching weather for {city}"
            )
            return None

        except requests.exceptions.Timeout as e:
            ExceptionHandler.handle_api_error(
                e,
                f"Timeout while fetching weather for {city}"
            )
            return None

        except requests.exceptions.HTTPError as e:
            ExceptionHandler.handle_api_error(
                e,
                f"HTTP error while fetching weather for {city}"
            )
            return None

        except requests.exceptions.RequestException as e:
            ExceptionHandler.handle_api_error(
                e,
                f"API request failed while fetching weather for {city}"
            )
            return None

        except ValueError as e:
            ExceptionHandler.handle_data_error(
                e,
                f"Invalid JSON response while fetching weather for {city}"
            )
            return None

        except KeyError as e:
            ExceptionHandler.handle_data_error(
                e,
                f"Missing weather data field for {city}"
            )
            return None

        except Exception as e:
            ExceptionHandler.handle_general_error(
                e,
                f"Unexpected error while fetching weather for {city}"
            )
            return None

    def get_forecast(self, city):

        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            response = requests.get(
                self.forecast_url,
                params=params,
                timeout=10
            )

            response.raise_for_status()
            data = response.json()

            forecast_list = []
            used_dates = set()

            for item in data["list"]:
                date_time = item["dt_txt"]
                date = date_time.split(" ")[0]
                time = date_time.split(" ")[1]

                if time == "12:00:00" and date not in used_dates:
                    forecast_info = {
                        "date": date,
                        "temperature": item["main"]["temp"],
                        "condition": item["weather"][0]["description"]
                    }

                    forecast_list.append(forecast_info)
                    used_dates.add(date)

                if len(forecast_list) == 5:
                    break

            return forecast_list

        except requests.exceptions.ConnectionError as e:
            ExceptionHandler.handle_api_error(
                e,
                f"Connection error while fetching forecast for {city}"
            )
            return []

        except requests.exceptions.Timeout as e:
            ExceptionHandler.handle_api_error(
                e,
                f"Timeout while fetching forecast for {city}"
            )
            return []

        except requests.exceptions.HTTPError as e:
            ExceptionHandler.handle_api_error(
                e,
                f"HTTP error while fetching forecast for {city}"
            )
            return []

        except requests.exceptions.RequestException as e:
            ExceptionHandler.handle_api_error(
                e,
                f"API request failed while fetching forecast for {city}"
            )
            return []

        except ValueError as e:
            ExceptionHandler.handle_data_error(
                e,
                f"Invalid JSON response while fetching forecast for {city}"
            )
            return []

        except KeyError as e:
            ExceptionHandler.handle_data_error(
                e,
                f"Missing forecast data field for {city}"
            )
            return []

        except Exception as e:
            ExceptionHandler.handle_general_error(
                e,
                f"Unexpected error while fetching forecast for {city}"
            )
            return []
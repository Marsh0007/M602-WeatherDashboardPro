import os
import matplotlib.pyplot as plt

from utils.exception_handler import ExceptionHandler


class ChartGenerator:

    def __init__(self):
        self.chart_folder = "charts"
        self.ensure_chart_folder_exists()

    def ensure_chart_folder_exists(self):
        try:
            if not os.path.exists(self.chart_folder):
                os.makedirs(self.chart_folder)

        except OSError as e:
            ExceptionHandler.handle_file_error(
                e,
                "Creating charts folder"
            )

    def generate_forecast_chart(self, city, forecast_data):
        if not forecast_data:
            return None

        try:
            dates = []
            temperatures = []

            for day in forecast_data:
                dates.append(day["date"])
                temperatures.append(float(day["temperature"]))

            plt.figure(figsize=(8, 5))

            plt.plot(
                dates,
                temperatures,
                marker="o",
                linewidth=2
            )

            plt.title(f"{city} - 5 Day Temperature Forecast")
            plt.xlabel("Forecast Date")
            plt.ylabel("Temperature (°C)")
            plt.grid(True, linestyle="--", alpha=0.5)

            plt.xticks(rotation=20)
            plt.tight_layout()

            chart_path = os.path.join(
                self.chart_folder,
                "forecast_temperature_chart.png"
            )

            plt.savefig(chart_path, dpi=120)
            plt.close()

            return chart_path

        except KeyError as e:
            ExceptionHandler.handle_data_error(
                e,
                "Missing forecast data field while generating chart"
            )
            return None

        except ValueError as e:
            ExceptionHandler.handle_data_error(
                e,
                "Invalid temperature value while generating chart"
            )
            return None

        except OSError as e:
            ExceptionHandler.handle_file_error(
                e,
                "File error while saving forecast chart"
            )
            return None

        except Exception as e:
            ExceptionHandler.handle_chart_error(
                e,
                "Unexpected error while generating forecast chart"
            )
            return None

        finally:
            plt.close()
import os
import csv

import tkinter as tk
import customtkinter as ctk


from tkinter import messagebox
from datetime import datetime
from tkinter import simpledialog
from weather_service import WeatherService
from alert_manager import AlertManager
from file_manager import FileManager
from city_manager import CityManager
from city_comparison import CityComparison
from chart_generator import ChartGenerator


class WeatherDashboardGUI:

    def __init__(self):
        self.weather_service = WeatherService()
        self.file_manager = FileManager()
        self.city_manager = CityManager()
        self.chart_generator = ChartGenerator()
        self.alert_manager = AlertManager()
        self.city_comparison = CityComparison()

        self.current_city = None
        self.current_forecast = []

        self.bg_color = "#F7F7F4"
        self.card_color = "#FFFFFF"
        self.soft_card = "#F3F1EA"
        self.alert_bg = "#F7EDDB"
        self.text_color = "#111827"
        self.muted_text = "#4B5563"
        self.border_color = "#D1D5DB"
        self.blue_color = "#2563EB"
        self.alert_text = "#7C5A18"

        ctk.set_appearance_mode("light")

        self.window = ctk.CTk()
        self.window.title("Weather Dashboard Pro")
        self.window.configure(fg_color=self.bg_color)
        self.window.geometry("900x820")
        self.window.resizable(False, False)

        self.create_widgets()
        self.update_clock()

    def create_card(self, parent, color=None, radius=12):
        return ctk.CTkFrame(
            parent,
            fg_color=color or self.card_color,
            corner_radius=radius,
            border_width=1,
            border_color=self.border_color
        )

    def create_widgets(self):
        self.page = ctk.CTkFrame(
            self.window,
            fg_color=self.bg_color,
            width=800
        )
        self.page.pack(pady=25)

        header = ctk.CTkFrame(self.page, fg_color=self.bg_color)
        header.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(
            header,
            text="☁  Weather Dashboard Pro",
            font=("Arial", 24, "bold"),
            text_color=self.text_color
        ).pack(side="left")

        self.clock_label = ctk.CTkLabel(
            header,
            text="",
            font=("Arial", 10),
            text_color=self.muted_text
        )
        self.clock_label.pack(side="right")

        search_frame = ctk.CTkFrame(self.page, fg_color=self.bg_color)
        search_frame.pack(fill="x", pady=(0, 18))

        self.city_entry = ctk.CTkEntry(
            search_frame,
            font=("Arial", 13),
            height=38,
            corner_radius=8,
            fg_color=self.card_color,
            text_color=self.text_color,
            border_color=self.border_color
        )
        self.city_entry.pack(side="left", fill="x", expand=True)

        ctk.CTkButton(
            search_frame,
            text="🔍  Get Weather",
            command=self.search_weather,
            width=150,
            height=38,
            corner_radius=8,
            fg_color=self.blue_color,
            hover_color="#1D4ED8",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=(10, 0))

        top_row = ctk.CTkFrame(self.page, fg_color=self.bg_color)
        top_row.pack(fill="x", pady=(0, 12))

        weather_card = self.create_card(top_row)
        weather_card.pack(side="left", padx=(0, 10))
        weather_card.configure(width=395, height=115)
        weather_card.pack_propagate(False)

        weather_content = ctk.CTkFrame(weather_card, fg_color=self.card_color)
        weather_content.pack(padx=22, pady=18, fill="both")

        self.weather_icon_label = ctk.CTkLabel(
            weather_content,
            text="☀",
            font=("Arial", 42),
            text_color=self.alert_text
        )
        self.weather_icon_label.pack(side="left", padx=(0, 25))

        weather_text_area = ctk.CTkFrame(weather_content, fg_color=self.card_color)
        weather_text_area.pack(side="left", anchor="center")

        temp_row = ctk.CTkFrame(weather_text_area, fg_color=self.card_color)
        temp_row.pack(anchor="w")

        self.temp_label = ctk.CTkLabel(
            temp_row,
            text="--°C",
            font=("Arial", 38, "bold"),
            text_color=self.text_color
        )
        self.temp_label.pack(side="left")

        self.feels_label = ctk.CTkLabel(
            temp_row,
            text="",
            font=("Arial", 12),
            text_color=self.muted_text
        )
        self.feels_label.pack(side="left", padx=(10, 0))

        self.weather_label = ctk.CTkLabel(
            weather_text_area,
            text="Search for a city to view weather.",
            font=("Arial", 12),
            text_color=self.muted_text,
            justify="left"
        )
        self.weather_label.pack(anchor="w", pady=(4, 0))

        alert_card = self.create_card(top_row, color=self.alert_bg)
        alert_card.pack(side="left")
        alert_card.configure(width=355, height=115)
        alert_card.pack_propagate(False)

        alert_content = ctk.CTkFrame(alert_card, fg_color=self.alert_bg)
        alert_content.pack(padx=18, pady=20, fill="both")

        ctk.CTkLabel(
            alert_content,
            text="⚠",
            font=("Arial", 20),
            text_color=self.alert_text
        ).pack(side="left", padx=(0, 14), anchor="n")

        alert_text_frame = ctk.CTkFrame(alert_content, fg_color=self.alert_bg)
        alert_text_frame.pack(side="left", fill="both", expand=True)

        self.alert_title_label = ctk.CTkLabel(
            alert_text_frame,
            text="Weather alert",
            font=("Arial", 13, "bold"),
            text_color=self.alert_text
        )
        self.alert_title_label.pack(anchor="w")

        self.alert_label = ctk.CTkLabel(
            alert_text_frame,
            text="Search a city to see weather alerts.",
            font=("Arial", 11),
            text_color=self.alert_text,
            justify="left",
            wraplength=260
        )
        self.alert_label.pack(anchor="w", pady=(3, 0))

        stats_row = ctk.CTkFrame(self.page, fg_color=self.bg_color)
        stats_row.pack(fill="x", pady=(0, 18))

        self.searches_value = self.create_stat_card(stats_row, "Searches", "0")
        self.favorites_value = self.create_stat_card(stats_row, "Favorites", "0")
        self.avg_temp_value = self.create_stat_card(stats_row, "Average temp", "--°C")
        self.comfort_value = self.create_stat_card(stats_row, "Comfort Score", "--")

        ctk.CTkLabel(
            self.page,
            text="5-day forecast",
            font=("Arial", 16, "bold"),
            text_color=self.text_color
        ).pack(anchor="w", pady=(0, 8))

        self.forecast_cards_frame = ctk.CTkFrame(self.page, fg_color=self.bg_color)
        self.forecast_cards_frame.pack(fill="x", pady=(0, 18))

        recommendation_card = self.create_card(self.page)
        recommendation_card.pack(fill="x", pady=(0, 18))

        self.recommendation_label = ctk.CTkLabel(
            recommendation_card,
            text="Search a city to get recommendations",
            font=("Arial", 13, "bold"),
            text_color=self.text_color
        )

        self.recommendation_label.pack(
            padx=20,
            pady=15,
            anchor="w"
        )

        bottom_row = ctk.CTkFrame(self.page, fg_color=self.bg_color)
        bottom_row.pack(fill="x")

        favorites_section = ctk.CTkFrame(bottom_row, fg_color=self.bg_color)
        favorites_section.pack(side="left", padx=(0, 14))

        ctk.CTkLabel(
            favorites_section,
            text="Favorite cities",
            font=("Arial", 16, "bold"),
            text_color=self.text_color
        ).pack(anchor="w", pady=(0, 8))

        self.favorites_frame = self.create_card(favorites_section)
        self.favorites_frame.pack()
        self.favorites_frame.configure(width=355, height=210)
        self.favorites_frame.pack_propagate(False)

        actions_section = ctk.CTkFrame(bottom_row, fg_color=self.bg_color)
        actions_section.pack(side="left", anchor="n")

        ctk.CTkLabel(
            actions_section,
            text="Actions",
            font=("Arial", 16, "bold"),
            text_color=self.text_color
        ).pack(anchor="w", pady=(0, 8))

        actions_grid = ctk.CTkFrame(actions_section, fg_color=self.bg_color)
        actions_grid.pack()

        actions_grid.grid_columnconfigure(0, weight=1)
        actions_grid.grid_columnconfigure(1, weight=1)

        self.create_action_button(actions_grid, "☆  Add favorite", self.add_current_city_to_favorites, 0, 0)
        self.create_action_button(actions_grid, "⌁  Chart", self.generate_chart, 0, 1)

        self.create_action_button(actions_grid, "⟳  History", self.show_search_history, 1, 0)
        self.create_action_button(actions_grid, "⚖  Compare cities", self.compare_cities, 1, 1)

        self.create_action_button(actions_grid,"🌍 Climate Analyzer",self.climate_analyzer,2,0,2)

        ctk.CTkLabel(
            self.page,
            text="Data provided by OpenWeatherMap API · Search history saved locally",
            font=("Arial", 10),
            text_color=self.muted_text
        ).pack(pady=(18, 0))

        self.load_favorites_to_listbox()
        self.update_statistics()
        self.show_empty_forecast()

    def create_stat_card(self, parent, title, value):
        card = ctk.CTkFrame(
            parent,
            fg_color=self.soft_card,
            corner_radius=10,
            width=175,
            height=82
        )
        card.pack(side="left", padx=(0, 12))
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 11),
            text_color=self.muted_text
        ).pack(anchor="w", padx=16, pady=(12, 0))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 25, "bold"),
            text_color=self.text_color
        )
        value_label.pack(anchor="w", padx=16, pady=(0, 10))

        return value_label

    def create_action_button(self, parent, text, command, row, column, colspan=1):
        button = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            height=38,
            corner_radius=8,
            fg_color=self.card_color,
            hover_color=self.soft_card,
            text_color=self.text_color,
            border_width=1,
            border_color=self.border_color,
            font=("Arial", 11, "bold")
        )

        button.grid(
            row=row,
            column=column,
            columnspan=colspan,
            sticky="nsew",
            padx=4,
            pady=4
        )

    def update_clock(self):
        current_time = datetime.now().strftime("%d %B %Y | %H:%M:%S")
        self.clock_label.configure(text=current_time)
        self.window.after(1000, self.update_clock)

    def get_weather_emoji(self, condition):
        condition = condition.lower()

        if "clear" in condition:
            return "☀"
        if "cloud" in condition:
            return "☁"
        if "rain" in condition:
            return "☔"
        if "snow" in condition:
            return "❄"
        if "storm" in condition or "thunder" in condition:
            return "⚡"
        if "mist" in condition or "fog" in condition or "haze" in condition:
            return "≋"
        return "☁"

    def update_statistics(self):
        history = self.file_manager.load_weather_history()
        favorites = self.city_manager.load_favorites()

        total_searches = len(history)
        total_favorites = len(favorites)
        avg_temp = "--"

        if history:
            temperatures = []

            for row in history:
                try:
                    temperatures.append(float(row["Temperature"]))
                except:
                    pass

            if temperatures:
                avg_temp = round(sum(temperatures) / len(temperatures), 1)

        self.searches_value.configure(text=str(total_searches))
        self.favorites_value.configure(text=str(total_favorites))
        self.avg_temp_value.configure(text=f"{avg_temp}°C")

    def search_weather(self):
        placeholder_text = "Enter city name..."
        city = self.city_entry.get().strip()

        if city == "":
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return

        self.display_weather_for_city(city)

    def display_weather_for_city(self, city):
        data = self.weather_service.get_weather(city)

        if data is None:
            messagebox.showerror("Weather Error", "Weather data could not be found.")
            return

        self.current_city = data["city"]

        recommendation = self.generate_weather_recommendation(data)

        self.recommendation_label.configure(
            text=recommendation
        )

        comfort = self.calculate_comfort_score(data)

        self.comfort_value.configure(
            text=f"{comfort}/100"
        )
        if comfort >= 80:
            rating = "Excellent ☀️"
        elif comfort >= 60:
            rating = "Good 🙂"
        elif comfort >= 40:
            rating = "Moderate 😐"
        else:
            rating = "Poor 🌧"

        self.weather_icon_label.configure(text=self.get_weather_emoji(data["condition"]))
        self.temp_label.configure(text=f"{data['temperature']}°C")
        self.feels_label.configure(text=f"feels {data['feels_like']}°C")

        weather_text = (
            f"⌾ {data['city']}, {data['country']} · {data['condition'].title()}\n"
            f"♢ {data['humidity']}%       ≋ {data['wind_speed']} m/s"
        )
        self.weather_label.configure(text=weather_text)

        alerts = self.alert_manager.generate_alerts(data)

        if alerts:
            first_alert = alerts[0]
            for symbol in ["🔥", "❄️", "💧", "💨", "☔", "🌨", "✅"]:
                first_alert = first_alert.replace(symbol, "")

            parts = first_alert.split(":", 1)

            if len(parts) == 2:
                self.alert_title_label.configure(text=f"Comfort: {rating}")
                self.alert_label.configure(text=parts[1].strip())
            else:
                self.alert_title_label.configure(text="Weather alert")
                self.alert_label.configure(text=first_alert.strip())

        self.file_manager.save_weather_data(data)
        self.show_forecast(city)
        self.update_statistics()

    def show_empty_forecast(self):
        for widget in self.forecast_cards_frame.winfo_children():
            widget.destroy()

        for index in range(5):
            self.create_forecast_card("--", "☁", "--°C", "No data", index)

    def create_forecast_card(self, date, icon, temp, condition, index):
        self.forecast_cards_frame.grid_columnconfigure(index, weight=1, uniform="forecast")

        card = ctk.CTkFrame(
            self.forecast_cards_frame,
            fg_color=self.card_color,
            corner_radius=10,
            border_width=1,
            border_color=self.border_color
        )
        card.grid(row=0, column=index, padx=5, pady=4, sticky="nsew")

        ctk.CTkLabel(card, text=date, font=("Arial", 10), text_color=self.muted_text).pack(pady=(8, 0))
        ctk.CTkLabel(card, text=icon, font=("Arial", 24), text_color=self.blue_color).pack()
        ctk.CTkLabel(card, text=temp, font=("Arial", 14, "bold"), text_color=self.text_color).pack()
        ctk.CTkLabel(card, text=condition, font=("Arial", 10), text_color=self.text_color, wraplength=100).pack(pady=(0, 6))

    def show_forecast(self, city):
        forecast = self.weather_service.get_forecast(city)
        self.current_forecast = forecast

        for widget in self.forecast_cards_frame.winfo_children():
            widget.destroy()

        if not forecast:
            self.show_empty_forecast()
            return

        for index, day in enumerate(forecast[:5]):
            self.create_forecast_card(
                day["date"],
                self.get_weather_emoji(day["condition"]),
                f"{day['temperature']}°C",
                day["condition"].title(),
                index
            )

    def load_favorites_to_listbox(self):
        for widget in self.favorites_frame.winfo_children():
            widget.destroy()

        favorites = self.city_manager.load_favorites()

        if not favorites:
            ctk.CTkLabel(
                self.favorites_frame,
                text="No favorite cities yet.",
                font=("Arial", 10),
                text_color=self.muted_text
            ).pack(anchor="w", padx=14, pady=12)
            return

        for city in favorites:
            row = ctk.CTkFrame(self.favorites_frame, fg_color=self.card_color)
            row.pack(fill="x", padx=14, pady=4)

            city_label = ctk.CTkLabel(
                row,
                text=city,
                font=("Arial", 12, "bold"),
                text_color=self.text_color
            )
            city_label.pack(side="left")

            city_label.bind(
                "<Double-Button-1>",
                lambda event, city_name=city: self.load_favorite_city(city_name)
            )

            ctk.CTkButton(
                row,
                text="×",
                command=lambda city_name=city: self.remove_favorite_by_name(city_name),
                width=24,
                height=22,
                corner_radius=6,
                fg_color=self.card_color,
                hover_color=self.soft_card,
                text_color=self.muted_text
            ).pack(side="right")

    def load_favorite_city(self, city):
        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, city)
        self.display_weather_for_city(city)

    def add_current_city_to_favorites(self):
        if self.current_city is None:
            messagebox.showwarning("Favorite Error", "Please search for a city first.")
            return

        self.city_manager.save_favorite_city(self.current_city)
        self.load_favorites_to_listbox()
        self.update_statistics()

    def remove_selected_favorite(self):
        messagebox.showinfo(
            "Remove Favorite",
            "Use the × button beside a city name to remove it."
        )

    def remove_favorite_by_name(self, city):
        self.city_manager.remove_favorite_city(city)
        self.load_favorites_to_listbox()
        self.update_statistics()

    def generate_chart(self):
        if self.current_city is None:
            messagebox.showwarning("Chart Error", "Please search for a city first.")
            return

        if not self.current_forecast:
            messagebox.showwarning("Chart Error", "Forecast data is not available yet.")
            return

        chart_path = self.chart_generator.generate_forecast_chart(
            self.current_city,
            self.current_forecast
        )

        if chart_path:
            os.startfile(os.path.abspath(chart_path))
        else:
            messagebox.showerror("Chart Error", "Chart could not be generated.")

    def show_search_history(self):
        history = self.file_manager.load_weather_history()

        if not history:
            messagebox.showinfo("Search History", "No weather history found.")
            return

        history_window = ctk.CTkToplevel(self.window)
        history_window.title("Search History")
        history_window.geometry("700x480")
        history_window.configure(fg_color=self.bg_color)

        ctk.CTkLabel(
            history_window,
            text="Search History",
            font=("Arial", 22, "bold"),
            text_color=self.text_color
        ).pack(pady=15)

        history_box = tk.Text(
            history_window,
            font=("Consolas", 11),
            width=78,
            height=22,
            bg=self.card_color,
            fg=self.text_color,
            relief="flat",
            padx=12,
            pady=12
        )
        history_box.pack(pady=10)

        history_box.insert(tk.END, f"{'Date':<22}{'City':<18}{'Temperature'}\n")
        history_box.insert(tk.END, "-" * 58 + "\n")

        for row in history:
            history_box.insert(
                tk.END,
                f"{row['Date']:<22}{row['City']:<18}{row['Temperature']} °C\n"
            )

        history_box.config(state="disabled")

    def compare_cities(self):
        city_input = self.city_entry.get().strip()

        if not city_input:
            messagebox.showwarning(
                "Compare Cities",
                "Enter cities separated by commas.\nExample: Berlin, London, Paris"
            )
            return

        city_names = [city.strip() for city in city_input.split(",")]

        if len(city_names) < 2:
            messagebox.showwarning("Compare Cities", "Please enter at least two cities.")
            return

        cities_data = []

        for city in city_names:
            data = self.weather_service.get_weather(city)

            if data:
                cities_data.append(data)

        if len(cities_data) < 2:
            messagebox.showerror("Compare Cities", "Could not retrieve enough city data.")
            return

        hottest = self.city_comparison.find_hottest_city(cities_data)
        coldest = self.city_comparison.find_coldest_city(cities_data)

        result = ""

        for city in cities_data:
            result += f"{city['city']}: {city['temperature']} °C\n"

        result += f"\n🔥 Hottest: {hottest['city']} ({hottest['temperature']} °C)\n"
        result += f"❄ Coldest: {coldest['city']} ({coldest['temperature']} °C)"

        messagebox.showinfo("Weather Comparison", result)

    def calculate_comfort_score(self, data):

        temp = float(data["temperature"])
        humidity = float(data["humidity"])
        wind = float(data["wind_speed"])

        score = 100

        score -= abs(temp - 22) * 2
        score -= humidity * 0.15
        score -= wind * 1.5

        score = max(0, min(100, round(score)))

        return score

    def analyze_country(self, csv_path, country_name):

        cities = []

        with open(csv_path, newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:
                cities.append(row["City"])

        results = []

        for city in cities:

            data = self.weather_service.get_weather(city)

            if data:
                results.append(
                    (
                        city,
                        float(data["temperature"])
                    )
                )

        if not results:
            messagebox.showerror(
                "Climate Analyzer",
                "No weather data available."
            )
            return

        results.sort(
            key=lambda x: x[1],
            reverse=True
        )

        hottest = results[0]
        coldest = results[-1]

        avg_temp = round(
            sum(temp for _, temp in results) / len(results),
            1
        )

        spread = round(
            hottest[1] - coldest[1],
            1
        )

        result_window = ctk.CTkToplevel(self.window)
        result_window.title(f"{country_name} Climate Analysis")
        result_window.geometry("600x550")
        result_window.configure(fg_color=self.bg_color)

        title = ctk.CTkLabel(
            result_window,
            text=f"🌍 {country_name} Climate Analysis",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=15)

        summary = (
            f"Average Temperature: {avg_temp}°C\n"
            f"🔥 Hottest City: {hottest[0]} ({hottest[1]}°C)\n"
            f"❄ Coldest City: {coldest[0]} ({coldest[1]}°C)\n"
            f"📊 Temperature Spread: {spread}°C"
        )

        summary_label = ctk.CTkLabel(
            result_window,
            text=summary,
            font=("Arial", 13),
            justify="left"
        )
        summary_label.pack(pady=10)

        ranking_frame = ctk.CTkFrame(
            result_window,
            corner_radius=10
        )
        ranking_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        ranking_text = tk.Text(
            ranking_frame,
            font=("Consolas", 12),
            relief="flat",
            padx=10,
            pady=10
        )

        ranking_text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        ranking_text.insert(
            tk.END,
            f"{'Rank':<6}{'City':<20}{'Temp'}\n"
        )

        ranking_text.insert(
            tk.END,
            "-" * 40 + "\n"
        )

        for rank, (city, temp) in enumerate(results, start=1):
            ranking_text.insert(
                tk.END,
                f"{rank:<6}{city:<20}{temp}°C\n"
            )

        ranking_text.config(state="disabled")

    def climate_analyzer(self):

        popup = ctk.CTkToplevel(self.window)
        popup.title("🌍 Climate Analyzer")
        popup.geometry("400x280")
        popup.resizable(False, False)

        ctk.CTkLabel(
            popup,
            text="Climate Analyzer",
            font=("Arial", 18, "bold")
        ).pack(pady=(15, 15))

        ctk.CTkLabel(
            popup,
            text="Select Continent"
        ).pack()

        continent_dropdown = ctk.CTkComboBox(
            popup,
            values=["Europe", "Asia", "Africa"]
        )
        continent_dropdown.pack(pady=5)

        ctk.CTkLabel(
            popup,
            text="Select Country"
        ).pack(pady=(15, 0))

        country_dropdown = ctk.CTkComboBox(
            popup,
            values=["Germany", "France", "Italy","Spain"]
        )
        country_dropdown.pack(pady=5)

        def update_countries(choice):

            if choice == "Europe":
                country_dropdown.configure(
                    values=["Germany", "France", "Italy","Spain"]
                )
                country_dropdown.set("Germany")

            elif choice == "Asia":
                country_dropdown.configure(
                    values=["India", "Japan", "China"]
                )
                country_dropdown.set("India")

            elif choice == "Africa":
                country_dropdown.configure(
                    values=["Egypt", "Nigeria", "South Africa"]
                )
                country_dropdown.set("Egypt")

        continent_dropdown.configure(
            command=update_countries
        )

        continent_dropdown.set("Europe")
        country_dropdown.set("Germany")

        def run_analysis():

            continent = continent_dropdown.get().lower()
            country = country_dropdown.get().lower().replace(" ", "_")

            csv_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "data",
                continent,
                f"{country}.csv"
            )

            if not os.path.exists(csv_path):
                messagebox.showerror(
                    "File Error",
                    f"Dataset not found:\n{csv_path}"
                )
                return

            popup.destroy()

            self.analyze_country(
                csv_path,
                country.title()
            )

        ctk.CTkButton(
            popup,
            text="Analyze",
            command=run_analysis,
            width=150,
            height=40
        ).pack(pady=25)



    def generate_weather_recommendation(self, data):

        temp = float(data["temperature"])
        humidity = float(data["humidity"])
        wind = float(data["wind_speed"])
        condition = data["condition"].lower()

        if "rain" in condition:
            return "🌧 Carry an umbrella"

        if temp < 5:
            return "❄ Wear warm clothes"

        if wind > 10:
            return "💨 Strong winds expected"

        if temp > 25:
            return "☀ Great day for outdoor activities"

        return "🙂 Pleasant weather today"

    def run(self):
        self.window.mainloop()
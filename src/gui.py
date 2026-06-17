import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from weather_service import WeatherService
from file_manager import FileManager
from city_manager import CityManager
from chart_generator import ChartGenerator
from rounded_button import RoundedButton
from theme import *


class WeatherDashboardGUI:

    def __init__(self):
        self.weather_service = WeatherService()
        self.file_manager = FileManager()
        self.city_manager = CityManager()
        self.chart_generator = ChartGenerator()

        self.current_forecast = []

        self.bg_color = BG_COLOR
        self.card_color = CARD_COLOR
        self.input_color = INPUT_COLOR
        self.text_color = TEXT_COLOR
        self.muted_text = MUTED_TEXT
        self.accent_color = ACCENT_COLOR
        self.blue_color = BLUE_COLOR
        self.green_color = GREEN_COLOR
        self.red_color = RED_COLOR

        self.window = tk.Tk()
        self.window.title("Weather Dashboard Pro")
        self.window.geometry("1120x720")
        self.window.config(bg=self.bg_color)
        self.window.resizable(False, False)

        self.create_scrollable_layout()
        self.create_widgets()
        self.update_clock()

    def create_scrollable_layout(self):
        self.canvas = tk.Canvas(
            self.window,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(
            self.window,
            orient="vertical",
            command=self.canvas.yview
        )
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.main_container = tk.Frame(self.canvas, bg=self.bg_color)

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.main_container,
            anchor="nw"
        )

        self.main_container.bind("<Configure>", self.update_scroll_region)
        self.canvas.bind("<Configure>", self.update_canvas_width)
        self.window.bind_all("<MouseWheel>", self.on_mousewheel)

    def update_scroll_region(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_canvas_width(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_card(self, parent, width, height):
        card = tk.Frame(
            parent,
            bg=self.card_color,
            padx=22,
            pady=20,
            width=width,
            height=height
        )
        card.pack(pady=10)
        card.pack_propagate(False)
        return card

    def create_section_title(self, parent, text):
        tk.Label(
            parent,
            text=text,
            font=SECTION_FONT,
            bg=self.card_color,
            fg=self.accent_color
        ).pack(anchor="w")

    def create_widgets(self):
        title_label = tk.Label(
            self.main_container,
            text="🌦 Weather Dashboard Pro",
            font=TITLE_FONT,
            bg=self.bg_color,
            fg=self.text_color
        )
        title_label.pack(pady=(20, 3))

        subtitle_label = tk.Label(
            self.main_container,
            text="Live weather, forecast, favorites, and temperature history",
            font=("Arial", 11),
            bg=self.bg_color,
            fg=self.muted_text
        )
        subtitle_label.pack(pady=(0, 5))

        self.clock_label = tk.Label(
            self.main_container,
            text="",
            font=("Arial", 11),
            bg=self.bg_color,
            fg=self.muted_text
        )
        self.clock_label.pack(pady=(0, 15))

        search_frame = tk.Frame(
            self.main_container,
            bg=self.card_color,
            padx=20,
            pady=15
        )
        search_frame.pack(pady=(0, 15))

        self.city_entry = tk.Entry(
            search_frame,
            font=("Arial", 14),
            width=34,
            bg=self.input_color,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief="flat"
        )
        self.city_entry.grid(row=0, column=0, padx=(0, 15), ipady=9)

        search_button = RoundedButton(
            search_frame,
            text="Get Weather",
            command=self.search_weather,
            bg_color=self.blue_color,
            hover_color=self.accent_color,
            width=150,
            height=45
        )
        search_button.grid(row=0, column=1)

        main_frame = tk.Frame(self.main_container, bg=self.bg_color)
        main_frame.pack()

        left_column = tk.Frame(main_frame, bg=self.bg_color)
        left_column.grid(row=0, column=0, padx=15, sticky="n")

        middle_column = tk.Frame(main_frame, bg=self.bg_color)
        middle_column.grid(row=0, column=1, padx=15, sticky="n")

        right_column = tk.Frame(main_frame, bg=self.bg_color)
        right_column.grid(row=0, column=2, padx=15, sticky="n")

        weather_card = self.create_card(left_column, 330, 360)
        self.create_section_title(weather_card, "Current Weather")

        self.weather_icon_label = tk.Label(
            weather_card,
            text="🌍",
            font=("Arial", 46),
            bg=self.card_color,
            fg=self.text_color
        )
        self.weather_icon_label.pack(pady=(12, 0))

        self.temp_label = tk.Label(
            weather_card,
            text="-- °C",
            font=("Arial", 34, "bold"),
            bg=self.card_color,
            fg="#38BDF8"
        )
        self.temp_label.pack(pady=(5, 0))

        self.weather_label = tk.Label(
            weather_card,
            text="Search for a city to view weather.",
            font=("Arial", 11),
            bg=self.card_color,
            fg=self.text_color,
            justify="center",
            wraplength=270
        )
        self.weather_label.pack(pady=(10, 0))

        stats_card = self.create_card(left_column, 330, 180)
        self.create_section_title(stats_card, "Statistics")

        self.stats_label = tk.Label(
            stats_card,
            text="Searches: 0\nFavorites: 0\nAverage Temp: -- °C",
            font=NORMAL_FONT,
            bg=self.card_color,
            fg=self.text_color,
            justify="left"
        )
        self.stats_label.pack(anchor="w", pady=(15, 0))

        forecast_card = self.create_card(middle_column, 360, 450)
        self.create_section_title(forecast_card, "5-Day Forecast")

        self.forecast_box = tk.Text(
            forecast_card,
            font=("Arial", 11),
            width=34,
            height=23,
            bg=self.card_color,
            fg=self.text_color,
            relief="flat",
            wrap="word"
        )
        self.forecast_box.pack(anchor="w", pady=(18, 0))
        self.forecast_box.insert(tk.END, "Forecast will appear here.")
        self.forecast_box.config(state="disabled")

        favorites_card = self.create_card(right_column, 330, 260)
        self.create_section_title(favorites_card, "Favorite Cities")

        tk.Label(
            favorites_card,
            text="Double-click a city to load weather.",
            font=SMALL_FONT,
            bg=self.card_color,
            fg=self.muted_text
        ).pack(anchor="w", pady=(3, 10))

        self.favorites_listbox = tk.Listbox(
            favorites_card,
            font=("Arial", 12),
            width=28,
            height=7,
            bg=self.input_color,
            fg=self.text_color,
            selectbackground=self.accent_color,
            selectforeground="white",
            relief="flat"
        )
        self.favorites_listbox.pack(anchor="w")
        self.favorites_listbox.bind("<Double-Button-1>", self.load_selected_favorite)

        actions_card = self.create_card(right_column, 330, 330)
        self.create_section_title(actions_card, "Actions")

        tk.Frame(actions_card, bg=self.card_color, height=10).pack()

        RoundedButton(
            actions_card,
            text="Add Current City",
            command=self.add_current_city_to_favorites,
            bg_color=self.blue_color,
            hover_color=self.accent_color,
            width=250,
            height=42
        ).pack(pady=6)

        RoundedButton(
            actions_card,
            text="Remove Favorite",
            command=self.remove_selected_favorite,
            bg_color=self.red_color,
            hover_color="#F87171",
            width=250,
            height=42
        ).pack(pady=6)

        RoundedButton(
            actions_card,
            text="Forecast Chart",
            command=self.generate_chart,
            bg_color=self.green_color,
            hover_color="#34D399",
            width=250,
            height=42
        ).pack(pady=6)

        RoundedButton(
            actions_card,
            text="View Search History",
            command=self.show_search_history,
            bg_color="#7C3AED",
            hover_color="#A78BFA",
            width=250,
            height=42
        ).pack(pady=6)

        footer_label = tk.Label(
            self.main_container,
            text="Data provided by OpenWeatherMap API | Search history is saved locally",
            font=SMALL_FONT,
            bg=self.bg_color,
            fg=self.muted_text
        )
        footer_label.pack(pady=(15, 25))

        self.load_favorites_to_listbox()
        self.update_statistics()

    def update_clock(self):
        current_time = datetime.now().strftime("%d %B %Y | %H:%M:%S")
        self.clock_label.config(text=current_time)
        self.window.after(1000, self.update_clock)

    def get_weather_emoji(self, condition):
        condition = condition.lower()

        if "clear" in condition:
            return "☀️"
        elif "cloud" in condition:
            return "☁️"
        elif "rain" in condition:
            return "🌧️"
        elif "snow" in condition:
            return "❄️"
        elif "storm" in condition or "thunder" in condition:
            return "⛈️"
        elif "mist" in condition or "fog" in condition or "haze" in condition:
            return "🌫️"
        else:
            return "🌍"

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

        self.stats_label.config(
            text=(
                f"Searches: {total_searches}\n"
                f"Favorites: {total_favorites}\n"
                f"Average Temp: {avg_temp} °C"
            )
        )

    def search_weather(self):
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

        self.weather_icon_label.config(
            text=self.get_weather_emoji(data["condition"])
        )

        self.temp_label.config(
            text=f"{data['temperature']} °C"
        )

        weather_text = (
            f"📍 {data['city']}, {data['country']}\n\n"
            f"🤔 Feels Like: {data['feels_like']} °C\n"
            f"💧 Humidity: {data['humidity']} %\n"
            f"☁ Condition: {data['condition'].title()}\n"
            f"💨 Wind: {data['wind_speed']} m/s"
        )

        self.weather_label.config(text=weather_text)

        self.file_manager.save_weather_data(data)
        self.show_forecast(city)
        self.update_statistics()

    def show_forecast(self, city):
        forecast = self.weather_service.get_forecast(city)
        self.current_forecast = forecast

        self.forecast_box.config(state="normal")
        self.forecast_box.delete("1.0", tk.END)

        if not forecast:
            self.forecast_box.insert(tk.END, "Forecast data could not be found.")
            self.forecast_box.config(state="disabled")
            return

        for day in forecast:
            forecast_text = (
                f"📅 {day['date']}\n"
                f"🌡 Temperature: {day['temperature']} °C\n"
                f"☁ Condition: {day['condition'].title()}\n"
                f"{'─' * 30}\n\n"
            )
            self.forecast_box.insert(tk.END, forecast_text)

        self.forecast_box.config(state="disabled")

    def add_current_city_to_favorites(self):
        if self.current_city is None:
            messagebox.showwarning("Favorite Error", "Please search for a city first.")
            return

        self.city_manager.save_favorite_city(self.current_city)
        self.load_favorites_to_listbox()
        self.update_statistics()

        messagebox.showinfo(
            "Favorite Added",
            f"{self.current_city} added to favorites."
        )

    def remove_selected_favorite(self):
        selected = self.favorites_listbox.curselection()

        if not selected:
            messagebox.showwarning("Remove Favorite", "Please select a favorite city.")
            return

        city = self.favorites_listbox.get(selected[0]).strip()

        self.city_manager.remove_favorite_city(city)
        self.load_favorites_to_listbox()
        self.update_statistics()

        messagebox.showinfo(
            "Favorite Removed",
            f"{city} removed successfully."
        )

    def load_favorites_to_listbox(self):
        self.favorites_listbox.delete(0, tk.END)

        favorites = self.city_manager.load_favorites()

        for city in favorites:
            self.favorites_listbox.insert(tk.END, f"  {city}")

    def load_selected_favorite(self, event):
        selected = self.favorites_listbox.curselection()

        if not selected:
            return

        selected_city = self.favorites_listbox.get(selected[0]).strip()

        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, selected_city)

        self.display_weather_for_city(selected_city)

    def generate_chart(self):
        if self.current_city is None:
            messagebox.showwarning(
                "Chart Error",
                "Please search for a city first."
            )
            return

        if not self.current_forecast:
            messagebox.showwarning(
                "Chart Error",
                "Forecast data is not available yet."
            )
            return

        chart_path = self.chart_generator.generate_forecast_chart(
            self.current_city,
            self.current_forecast
        )

        if chart_path:
            absolute_path = os.path.abspath(chart_path)
            os.startfile(absolute_path)

            messagebox.showinfo(
                "Chart Generated",
                f"Forecast chart generated successfully.\n\nSaved at:\n{absolute_path}"
            )
        else:
            messagebox.showerror(
                "Chart Error",
                "Chart could not be generated."
            )

    def show_search_history(self):
        history = self.file_manager.load_weather_history()

        if not history:
            messagebox.showinfo("Search History", "No weather history found.")
            return

        history_window = tk.Toplevel(self.window)
        history_window.title("Search History")
        history_window.geometry("700x480")
        history_window.config(bg=self.bg_color)

        title_label = tk.Label(
            history_window,
            text="Search History",
            font=("Arial", 22, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title_label.pack(pady=15)

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

        header = f"{'Date':<22}{'City':<18}{'Temperature'}\n"
        separator = "-" * 58 + "\n"

        history_box.insert(tk.END, header)
        history_box.insert(tk.END, separator)

        for row in history:
            line = (
                f"{row['Date']:<22}"
                f"{row['City']:<18}"
                f"{row['Temperature']} °C\n"
            )
            history_box.insert(tk.END, line)

        history_box.config(state="disabled")

    def run(self):
        self.window.mainloop()
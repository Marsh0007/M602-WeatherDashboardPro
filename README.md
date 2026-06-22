# WeatherDashboardPro (M602 Computer Programming Project)

A modern desktop weather application built with Python, CustomTkinter, and the OpenWeatherMap API.

## Features

### Current Weather

* Real-time weather retrieval
* Temperature
* Humidity
* Wind Speed
* Weather Condition
* Weather Alerts

### 5-Day Forecast

* Dynamic forecast cards
* Daily temperature predictions
* Weather condition display
* Forecast trend overview

### Favorites Management

* Save favorite cities
* Remove favorites
* Quick city access

### Search History

* Track previous searches
* Local data persistence

### Weather Comfort Score

Custom weather scoring algorithm based on:

* Temperature
* Humidity
* Wind Speed

Score range:

* 0–100

### Weather Recommendation Engine

Provides recommendations such as:

* Carry an umbrella
* Wear warm clothes
* Strong winds expected
* Great day for outdoor activities

### Climate Analyzer

Analyze weather conditions across multiple cities within a selected country.

Supported Continents:

* Europe
* Asia
* Africa

Features:

* Hottest City Detection
* Coldest City Detection
* Average Temperature Calculation
* Temperature Spread Analysis
* City Temperature Ranking

### Data Visualization

* Temperature trend charts
* Forecast graph generation
* Matplotlib integration

---

## Technologies Used

* Python 3
* CustomTkinter
* OpenWeatherMap API
* Matplotlib
* CSV File Handling
* JSON Processing

---

## Project Structure

```text
WeatherDashboardPro/
│
├── data/
│   ├── Africa/
│   ├── Asia/
│   ├── europe/
│   ├── favorites.json
│   └── weather_history.csv
│
├── src/
│   ├── charts/
│   │   └── forecast_temperature_chart.png
│   │
│   ├── logs/ (The Folder folder will created automactically whenever the user creates any error with error log file)
│   │   └── error.log
│   │
│   ├── utils/
│   │   └── exception_handler.py
│   │
│   ├── alert_manager.py
│   ├── chart_generator.py
│   ├── city_comparison.py
│   ├── city_manager.py
│   ├── file_manager.py
│   ├── gui.py
│   ├── main.py
│   ├── rounded_button.py
│   ├── theme.py
│   └── weather_service.py
│
├── .env
├── .gitignore
└── README.md
```

```

---

## Installation

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root (Put your Weather API Key)

```env
API_KEY=YOUR_OPENWEATHERMAP_API_KEY
```

3. Run the application

```bash
python src/main.py
```

---

## Climate Analyzer Algorithm

1. Load city data from CSV files.
2. Retrieve live weather data using OpenWeatherMap API.
3. Store city-temperature pairs.
4. Sort temperatures in descending order.
5. Calculate:

   * Hottest City
   * Coldest City
   * Average Temperature
   * Temperature Spread
6. Display ranked results.
7. 

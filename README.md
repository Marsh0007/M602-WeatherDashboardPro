# WeatherDashboardPro (M602 Computer Programming Project)

A Python desktop application built using Tkinter and the OpenWeatherMap API.

## Features

* Current weather information
* 5-Day weather forecast
* Favorite cities management
* Forecast temperature chart visualization
* Search history tracking
* Statistics dashboard
* Centralized exception handling
* Object-Oriented Programming (OOP) architecture

## Technologies Used

* Python
* Tkinter
* OpenWeatherMap API
* Requests
* Matplotlib
* JSON
* CSV
* python-dotenv

## Project Structure

```text
WeatherDashboardPro/
│
├── data/
│   ├── favorites.json
│   └── weather_history.csv
│
├── charts/
│   └── forecast_temperature_chart.png
│
├── src/
│   ├── utils/
│   │   └── exception_handler.py
│   │
│   ├── weather_service.py
│   ├── city_manager.py
│   ├── file_manager.py
│   ├── chart_generator.py
│   ├── rounded_button.py
│   ├── theme.py
│   ├── gui.py
│   └── main.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```



## Installation

1. Install dependencies

```bash
pip install requests matplotlib python-dotenv
```

2. Create a `.env` file in the project root

```env
API_KEY=YOUR_OPENWEATHERMAP_API_KEY
```

3. Run the application

```bash
python src/main.py
```



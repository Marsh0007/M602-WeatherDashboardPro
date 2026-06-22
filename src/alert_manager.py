class AlertManager:
    """Creates simple weather alerts using if/elif conditions."""

    def generate_alerts(self, weather_data):
        alerts = []

        temperature = weather_data["temperature"]
        humidity = weather_data["humidity"]
        wind_speed = weather_data["wind_speed"]
        condition = weather_data["condition"].lower()

        if temperature >= 30:
            alerts.append("🔥 Heat alert: Drink water and avoid direct sunlight.")
        elif temperature <= 0:
            alerts.append("❄️ Freezing alert: Wear warm clothes.")

        if humidity >= 80:
            alerts.append("💧 High humidity: It may feel uncomfortable outside.")

        if wind_speed >= 10:
            alerts.append("💨 Wind alert: Be careful outside.")

        if "rain" in condition:
            alerts.append("☔ Rain alert: Carry an umbrella.")

        if "snow" in condition:
            alerts.append("🌨 Snow alert: Roads may be slippery.")

        if not alerts:
            alerts.append("✅ Weather looks normal today.")

        return alerts
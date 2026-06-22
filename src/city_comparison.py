class CityComparison:
    """Compares weather data from multiple cities."""

    def find_hottest_city(self, cities_data):
        if not cities_data:
            return None

        hottest = cities_data[0]

        for city in cities_data:
            if city["temperature"] > hottest["temperature"]:
                hottest = city

        return hottest

    def find_coldest_city(self, cities_data):
        if not cities_data:
            return None

        coldest = cities_data[0]

        for city in cities_data:
            if city["temperature"] < coldest["temperature"]:
                coldest = city

        return coldest
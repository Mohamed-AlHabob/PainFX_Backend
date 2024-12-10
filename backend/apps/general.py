import googlemaps
from django.conf import settings

class GeolocationService:
    @staticmethod
    def fetch_coordinates(address):
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return f"{location['lat']},{location['lng']}"
        raise ValueError("Geolocation not found")

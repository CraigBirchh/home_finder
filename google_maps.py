import googlemaps
import pandas as pd
from constants import ApiKeys, Headings

class GoogleMaps:
    def __init__(self):
        api_key = ApiKeys.GOOGLEMAPS.value
        self.gmaps = googlemaps.Client(key=api_key)

    def get_distances(self, addresses, urls, destination):
        rows = []
        for index, address in enumerate(addresses):
            row = self._get_distance(address, destination)
            row.append(urls[index])
            rows.append(row)
        return pd.DataFrame(rows)

    def _get_distance(self, origin, destination):
        distances = []

        # Get Distance km
        result = self.gmaps.distance_matrix(origin, destination, mode="driving")
        distance_m = result['rows'][0]['elements'][0]['distance']['value']
        distance_km = distance_m / 1000
        distances.append(distance_km)

        # Travel modes to check
        modes = Headings.MAP_METHODS.value
        for mode in modes:
            result = self.gmaps.distance_matrix(origin, destination, mode=mode)
            duration = result['rows'][0]['elements'][0]['duration']['text']
            distances.append(duration)

        return distances
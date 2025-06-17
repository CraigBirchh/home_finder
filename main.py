from copy import deepcopy
import json
from constants import Configs, LocationConfigKeys, FileConfigKeys, Locations
from rightmove import Rightmove
from google_maps import GoogleMaps
from property_organiser import PropertyOrganiser

class app_runner:
    def __init__(self, location_config_path, file_config_path):
        # Initalise Configs
        self.location_config = self.load_config(location_config_path)
        self.file_config = self.load_config(file_config_path)

        # Initalise Main Classes
        self.organiser = PropertyOrganiser(self.file_config[FileConfigKeys.CURRENT_SEARCH.value])
        self.rightmove = Rightmove()
        self.googlemaps = GoogleMaps()

        while True:
            choice = input("A) Full Search (Config Area),\n"
                           "B) Full Search (New Area),\n"
                           "C) Link Search \n"
                           "E) Review List,\n"
                           "F) Create CSV for My Maps,\n "
                           "H) Quit\n"
                           "Enter a command: ").upper()

            match choice:
                case "A":
                    self.full_search(self.location_config[LocationConfigKeys.LOCATION.value])
                case "B":
                    location = input("Please enter a location ")
                    self.full_search(location)
                case "C":
                    self.link_search()
                case "D":
                    self.organiser.review_df()
                    pass
                case "E":
                    self.organiser.convert_to_csv(self.file_config[FileConfigKeys.MY_MAPS.value])
                case "F":
                    print("Exiting...")
                    break
                case _:
                    print("Unknown command")

    def load_config(self, file_path):
        with open(file_path, 'r') as f:
            file_config = json.load(f)
            return deepcopy(file_config)

    def full_search(self, location):
            self.organiser.add_from_api(self.rightmove.get_properties(self.location_config, location))
            self.organiser.add_from_scraper(self.rightmove.scrape_properties(self.location_config,
                                            self.organiser.df["URL"]))
            self.organiser.delete_from_scraper(self.rightmove.refine_properties(self.location_config))
            self.organiser.add_from_scraper(self.googlemaps.get_distances(self.organiser.df["URL"],
                                            self.organiser.df["Address"], Locations.WORK_LOCATION.value))
            self.organiser.convert_to_csv(self.file_config[FileConfigKeys.MY_MAPS.value])

    def link_search(self):
            urls = self.organiser.get_urls(self.file_config[FileConfigKeys.LINK_SEARCH.value])
            self.organiser.add_from_api(self.rightmove.research_properties(urls))
            self.organiser.delete_from_scraper(self.rightmove.refine_properties(self.location_config, self.organiser.df))
            self.organiser.add_from_scraper(self.googlemaps.get_distances(self.organiser.df["URL"],
                                            self.organiser.df["Address"], Locations.WORK_LOCATION.value))
            self.organiser.convert_to_csv(self.file_config[FileConfigKeys.MY_MAPS.value])


def main():
    print("Home Finder")
    ap = app_runner(Configs.LOCATION.value, Configs.FILES.value)
    print("Fin")

if __name__ == "__main__":
    main()
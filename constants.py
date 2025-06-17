from enum import Enum, unique

@unique
class Configs(Enum):
    LOCATION = "config/location.config"
    FILES = "config/files.config"


@unique
class Drivers(Enum):
    WEB_DRIVER = r"msedgedriver.exe"


@unique
class ApiKeys(Enum):
    GOOGLEMAPS = "AIzaSyDXwADkH7O9iXuKNOYkWsZTdN-1iI3LwHQ"

@unique
class Headings(Enum):
    DATAFRAME = ["Address", "URL", "Price", "Bedrooms", "Added", "Property Type"
                 "Let Available Date", "Deposit", "Min. Tenancy", "Furnish Type",
                 "Bathrooms", "Size", "Distance", "Driving", "Public Transport", "Cycling", "Walking"]

    SITE_SCRAPE = {"Address": 'streetAddress',
                   "Price": 'pcm',
                   "Bedrooms": 'BEDROOMS',
                   "Added": "^(Added|Reduced)",
                   "Property Type": 'PROPERTY TYPE'
                    }

    LINK_SCRAPER = {"Let Available Date": 'Let available date: ',
                    "Deposit": 'Deposit: ',
                    "Min. Tenancy": 'Min. Tenancy: ',
                    "Furnish Type": 'Furnish type: ',
                    "Bathrooms":'BATHROOMS',
                    "Size": 'SIZE'
                    }

    MAP_METHODS = ["driving", "transit", "bicycling", "walking"]


@unique
class Locations(Enum):
    WORK_LOCATION = "3-7 Herbal Hill, London EC1R 5EJ"


@unique
class Links(Enum):
    RIGHTMOVE_RENT = "https://www.rightmove.co.uk/property-to-rent"
    RIGHTMOVE_BUY = "https://www.rightmove.co.uk/property-for-sale"


@unique
class FileConfigKeys(Enum):
    CURRENT_SEARCH = "CurrentSearch"
    LINK_SEARCH = "LinkSearch"
    MY_MAPS = "MyMapsCsv"


@unique
class LocationConfigKeys(Enum):
    ACQUISITION_TYPE = "AcquisitionType"
    LOCATION ="Location"
    MIN_PRICE = "MinPrice"
    MAX_PRICE = "MaxPrice"
    MIN_BED = "MinBed"
    MAX_BED = "MaxBed"
    MIN_SIZE = "MinSize"
    MAX_SIZE = "MaxSize"
    MIN_BATH = "MinBath"
    MAX_BATH = "MaxBath",
    FURNISHED ="Furnished",
    MIN_TENANCY = "MinTenancyMonths"

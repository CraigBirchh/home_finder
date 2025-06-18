from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import urlencode, urlparse, parse_qs, unquote
import time
from constants import Links, Drivers

class RightmoveUrlRetriever:
    def __init__(self, buy_or_rent):
        if buy_or_rent.lower() == "rent":
            self.url = Links.RIGHTMOVE_RENT.value
        elif buy_or_rent.lower() == "buy":
            self.url = Links.RIGHTMOVE_BUY.value
        else:
            raise Exception(f"Invalid value for buy_or_rent: {buy_or_rent}")

        edge_service = Service(executable_path=Drivers.WEB_DRIVER.value)

        edge_options = Options()
        self.driver = webdriver.Edge(service=edge_service, options=edge_options)

    def get_region_id(self, location):
        try:
            self.driver.get(self.url)
            wait = WebDriverWait(self.driver, 15)

            # Accept cookies
            try:
                wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
                print("Cookies accepted")
            except:
                raise Exception("Cookie banner not shown")

            # Type and select location
            input_box = wait.until(EC.element_to_be_clickable((By.ID, "ta_searchInput")))
            input_box.clear()
            input_box.send_keys(location)
            print("Typed location")
            time.sleep(1)
            input_box.send_keys(Keys.ARROW_DOWN)
            input_box.send_keys(Keys.ENTER)
            print("Selected first suggestion with keyboard")

            # Click the "To Rent" button directly
            rent_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='toRentCta']")))
            rent_button.click()
            print("Clicked 'To Rent' button")

            # Wait for final URL with locationIdentifier
            wait.until(EC.url_contains("locationIdentifier"))
            print("🔗 Final URL:", self.driver.current_url)

            # Extract locationIdentifier from final URL
            parsed_url = urlparse(self.driver.current_url)
            query_params = parse_qs(parsed_url.query)

            location_id = query_params.get("locationIdentifier", [None])[0]

            if location_id:
                location_id = unquote(location_id)  # Decode if it's URL-encoded like REGION%5E93965
                print("Extracted locationIdentifier:", location_id)
                return location_id
            raise Exception("locationIdentifier not found")
        finally:
            self.driver.quit()

    def get_url(self, location_id, min_price, max_price, min_bed, max_bed):
        if not location_id:
            raise Exception("No Region Id Given")
        params = {
            "useLocationIdentifier": "true",
            "locationIdentifier": location_id,
            "rent": "To rent"
        }

        if min_price is not None:
            params["minPrice"] = min_price
        if max_price is not None:
            params["maxPrice"] = max_price
        if min_bed is not None:
            params["minBedrooms"] = min_bed
        if max_bed is not None:
            params["maxBedrooms"] = max_bed

        url = "https://www.rightmove.co.uk/property-to-rent/find.html?" + urlencode(params)
        print("🏡 Final Find URL:", url)
        return url
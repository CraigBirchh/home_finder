import requests
from bs4 import BeautifulSoup
from constants import Headings, LocationConfigKeys as LocKeys
import pandas as pd
import re
class RightmoveLinkScraper:
    def __init__(self, links):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        self.links = links

    def refine_rentals(self, config, df):
        removals = []
        for index, row in df.iterrows():
            if LocKeys.MIN_BATH.value in config:
                if row["Bathrooms"] < config[LocKeys.MIN_BATH.value]:
                    removals.append(row["URL"])
            if LocKeys.MAX_BATH.value in config:
                if row["Bathrooms"] > config[LocKeys.MAX_BATH.value]:
                    removals.append(row["URL"])
            if LocKeys.MIN_SIZE.value in config:
                if row["Size"] < config[LocKeys.MIN_SIZE.value]:
                    removals.append(row["URL"])
            if LocKeys.MAX_SIZE.value in config:
                if row["Size"] > config[LocKeys.MAX_SIZE.value]:
                    removals.append(row["URL"])
            if LocKeys.FURNISHED.value in config:
                if row["Furnish Type"] != config[LocKeys.FURNISHED.value]:
                    removals.append(row["URL"])
            if LocKeys.MIN_TENANCY.value in config:
                if row["Min. Tenancy"] < config[LocKeys.MIN_TENANCY.value]:
                    removals.append(row["URL"])
        return removals

    def research_rentals(self):
        rows = []
        d1 = Headings.SITE_SCRAPE.value
        d2 = Headings.LINK_SCRAPER.value
        d1.update(d2)

        for link in self.links:
            row = self._get_rental_data(link, d1)
            rows.append(row)
        return pd.DataFrame(rows)

    def get_rentals(self):
        rows = []
        d1 = Headings.LINK_SCRAPER.value

        for link in self.links:
            row = self._get_rental_data(link, d1)
            rows.append(row)
        return pd.DataFrame(rows)

    def _get_rental_data(self, url, scrape_data):
        self.soup = self._get_soup(url)

        row = {}
        row["URL"] = url
        for key, data in scrape_data.items():
            row[key] = self._scrape_data(key, data)

        return row

    def _scrape_data(self, key, data):
        if key in ["Let Available Date", "Deposit", "Min. Tenancy", "Furnish Type"]:
            dt = self.soup.find('dt', string=data)
            if dt:
                return dt.find_next_sibling('dd').text.strip()
            else:
                return (f"{key} not found")

        elif key in ["Bedrooms", "Bathrooms", "Size", "Property Type"]:
            span = self.soup.find('span', string=data)
            if span:
                return span.find_parent('dt').find_next_sibling('dd').get_text(strip=True)
            else:
                return (f"{key} not found")

        elif key == "Price":
            span = self.soup.find('span', string=lambda text: text and (data in text))
            if span:
                return span.text.strip()
            else:
                return (f"{key} not found")

        elif key == "Address":
            h1 = self.soup.find('h1', itemprop=data)
            if h1:
                h1.text.strip()
            else:
                return (f"{key} not found")

        elif key == "Added":
            for div in self.soup.find_all("div"):
                text = div.get_text(strip=True)
                if re.match(data, text):
                    return text
            return (f"{key} not found")

        else:
            raise Exception("Invalid Key")

    def _get_soup(self, url):
        response = requests.get(url, headers=self.headers)
        return BeautifulSoup(response.text, 'html.parser')
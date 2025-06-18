from rightmove_data import RightmoveData
from rightmove_url_retriever import RightmoveUrlRetriever
from rightmove_link_scraper import RightmoveLinkScraper
from constants import LocationConfigKeys

class Rightmove():
    def get_properties(self, config, location):
        rm_url_retriever = RightmoveUrlRetriever(config[LocationConfigKeys.ACQUISITION_TYPE.value])
        region_id = rm_url_retriever.get_region_id(location)
        filtered_url = rm_url_retriever.get_url(region_id,
                                                min_price=config[LocationConfigKeys.MIN_PRICE.value],
                                                max_price=config[LocationConfigKeys.MAX_PRICE.value],
                                                min_bed=config[LocationConfigKeys.MIN_BED.value],
                                                max_bed=config[LocationConfigKeys.MAX_BED.value])
        self.rm_data = RightmoveData(filtered_url)
        return self.rm_data.get_results

    def scrape_properties(self, links):
        rm_link_scraper = RightmoveLinkScraper(links)
        return rm_link_scraper.get_rentals()

    def research_properties(self, links):
        rm_link_scraper = RightmoveLinkScraper(links)
        return rm_link_scraper.research_rentals()

    def refine_properties(self, config, df):
        rm_link_scraper = RightmoveLinkScraper(df["URL"])
        return rm_link_scraper.refine_rentals(config, df)
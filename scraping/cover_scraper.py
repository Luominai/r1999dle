import json
from scraper import Scraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import unquote
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
import re

class CoverScraper(Scraper):
    def __init__(self, output_path, overviews_path):
        super().__init__(output_path)
        self.overviews_path = overviews_path

    def get_pages_to_scrape(self):
        overviews = {}
        with open(self.overviews_path, "r") as file:
            overviews = json.load(file)
        
        for name, overview in overviews.items():
            self.pages.append(overview["page"])
            self.data[name] = {}

        if self.force_update:
            return

        covers = {}
        try:
            with open(self.output_path, "r") as file:
                covers = json.load(file)
        except FileNotFoundError:
            return

        for name, cover in covers.items():
            if CoverScraper.is_complete(cover):
                self.pages.remove(overviews[name]["page"])
                self.data[name] = cover

    def parse_page(self, page):
        # print(f"parsing {page}")
        driver = webdriver.Firefox(options=self.options)
        driver.get(page)
        
        url_parts = page.split("/")
        lookup_name = unquote(str(url_parts[-1]))

        cover_info = ["proportions", "medium", "fragrance", "inspo", "signature", "release"]
        tag_names = ["div", "div", "div", "div", "a", "div"]
        output_fields = ["dimensions", "medium", "fragrance", "inspiration", "signature", "release"]
        cells = [CoverScraper.find_cell(driver, cover_info[i], tag_names[i]) for i in range(len(cover_info))]
        
        for i, cell in enumerate(cells):
            field = output_fields[i]
            # If cell is none, we have an error. Print the error
            if cell is None:
                print(f"failed to get {field} for ${page}")
            # Signature requires special handling because it is an img
            elif field == "signature":
                self.data[lookup_name][field] = Scraper.get_lazy_loaded_img(cell, "href")
            # Release needs a bit more parsing
            elif field == "release":
                text = cell.get_attribute("innerText")
                if text is not None:
                    dates = [s for s in text.split("\n") if s != ""]
                    dates = [s.replace(",", "") for s in dates]
                    dates = [" ".join(s.split(" ")[:3]) for s in dates]
                    self.data[lookup_name][field] = dates
            # All other fields can be found in innerHTML
            else:
                self.data[lookup_name][field] = cell.get_attribute("innerText")

        driver.quit()

    @staticmethod
    def is_complete(cover):
        fields = ["dimensions", "medium", "fragrance", "inspiration", "signature"]
        for field in fields:
            if field not in cover:
                return False
        return True

    @staticmethod
    def find_cell(driver: WebDriver, info_type: str, tag_name) -> WebElement | None:
        try:
            return driver.find_element(By.CSS_SELECTOR, f"[data-source={info_type}]").find_element(By.TAG_NAME, tag_name)
        except NoSuchElementException:
            return None

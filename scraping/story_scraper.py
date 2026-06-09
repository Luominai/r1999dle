import json
from scraper import Scraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import unquote
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver

class StoryScraper(Scraper):
    def __init__(self, output_path, overviews_path):
        super().__init__(output_path)
        self.overviews_path = overviews_path

    def get_pages_to_scrape(self):
        overviews = {}
        with open(self.overviews_path, "r") as file:
            overviews = json.load(file)
        
        for name, overview in overviews.items():
            self.pages.append(overview["page"] + "/Story")
            self.data[name] = {}

        if self.force_update:
            return

        stories = {}
        try:
            with open(self.output_path, "r") as file:
                stories = json.load(file)
        except FileNotFoundError:
            return

        for name, story in stories.items():
            if StoryScraper.is_complete(story):
                self.pages.remove(overviews[name]["page"] + "/Story")
                self.data[name] = story

    def parse_page(self, page):
        # print(f"parsing ${page}")
        url_parts = page.split("/")
        character_name = str(url_parts[-2])

        driver = webdriver.Firefox(options=self.options)
        driver.get(page)

        story_items: list[str] = [
            f"[data-image-key='{character_name}_Item_1.png']", 
            f"[data-image-key='{character_name}_Item_2.png']",
            f"[data-image-key='{character_name}_Item_3.png']"
        ]

        try:
            Scraper.scroll_to(driver, driver.find_element(By.CSS_SELECTOR, story_items[0]))
        except NoSuchElementException:
            print(f"could not find story item 1 for {page}")
            driver.quit()
            return

        story_item_urls = []

        for item in story_items:
            try:
                element = driver.find_element(By.CSS_SELECTOR, item)
                image = Scraper.get_lazy_loaded_img(element, "src")
                story_item_urls.append(image)
            except NoSuchElementException:
                print(f"no element with {item} on {page}")

        self.data[unquote(character_name)]["items"] = story_item_urls
        driver.quit()

    @staticmethod
    def is_complete(story):
        return "items" in story and len(story["items"]) >= 3
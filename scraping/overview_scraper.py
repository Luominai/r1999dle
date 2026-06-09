from scraper import Scraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import unquote

class OverviewScraper(Scraper):
    def get_pages_to_scrape(self, force_update = False):
        self.pages = [self.r1999_wiki + "/Crew_Members"]

    def parse_page(self, page):
        print(f"parsing {page}")
        driver = webdriver.Firefox(options=self.options)
        driver.get(page)
        table_body = driver.find_element(By.TAG_NAME, "tbody")
        rows = table_body.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            Scraper.scroll_to(driver, row)
            cells = row.find_elements(By.TAG_NAME, "td")
            try:
                [_, image_cell, name_cell, rarity_cell, afflatus_cell, damage_cell, tags_cell, birthday_cell, age_cell] = cells
            except ValueError:
                continue
            
            # get the character's overview data
            overview = {}
            try:
                overview["display_name"] = name_cell.find_element(By.TAG_NAME, "a").text
            except:
                print(f"error getting name. skipping")
                continue

            try:
                overview["image"] = Scraper.get_lazy_loaded_img(image_cell.find_element(By.TAG_NAME, "img"), "src")
            except:
                print(f"error getting image for {overview["display_name"]}")

            try:
                overview["character_page"] = str(name_cell.find_element(By.TAG_NAME, "a").get_attribute("href"))
                overview["lookup_name"] = unquote(overview["character_page"].split("/")[-1])
            except:
                print(f"error getting character page for {overview["display_name"]}")

            try:
                overview["rarity"] = int(rarity_cell.text)
            except:
                print(f"error getting rarity for {overview["display_name"]}")

            try:
                overview["afflatus"] = afflatus_cell.find_element(By.TAG_NAME, "a").text
            except:
                print(f"error getting afflatus for {overview["display_name"]}")

            try:
                overview["damage"] = damage_cell.text
            except:
                print(f"error getting damage type for {overview["display_name"]}")

            try:
                overview["tags"] = tags_cell.text.split("\n")
            except:
                print(f"error getting tags for {overview["display_name"]}")

            try:
                overview["birthday"] = birthday_cell.text
            except:
                print(f"error getting birthday for {overview["display_name"]}")

            try:
                overview["age"] = age_cell.text
            except:
                print(f"error getting age for {overview["display_name"]}")

            # print(overview)
            try:
                self.data[overview["lookup_name"]] = overview
            except:
                self.data[overview["display_name"]] = overview
        driver.quit()
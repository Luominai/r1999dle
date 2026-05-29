import json
import time
import threading
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from utils import get_lazy_loaded_img, scroll_to

r1999_wiki = "https://reverse1999.fandom.com/wiki/37/Story"
options = Options()
options.page_load_strategy = "eager"
# options.add_argument("--headless=new")

driver = webdriver.Firefox(options=options)
driver.get(r1999_wiki)
# driver.find_element(By.CSS_SELECTOR, f"[data-image-key='37_Item_1.png']")
print(driver.find_element(By.TAG_NAME, "figure").get_attribute("innerHTML"))


import json
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver

# I want to use eager load strategy, but it sometimes means I don't get links to lazy loaded images. This functions helps solve the issue
def get_lazy_loaded_img(cell: WebElement, attribute):
    image = cell.get_attribute(attribute)
    while not str(image).startswith("https"):
        time.sleep(0.1)
        image = cell.get_attribute(attribute)

    return image

# only chrome has a built in scrollTo function in selenium, but all browsers can replicate the effect with JS
def scroll_to(driver: WebDriver, element: WebElement):
    driver.execute_script("arguments[0].scrollIntoView()", element)
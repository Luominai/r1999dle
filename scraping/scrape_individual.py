import json
import time
import threading
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from selenium.webdriver.remote.webdriver import WebDriver
from scraping.utils import get_lazy_loaded_img, scroll_to

options = Options()
options.page_load_strategy = "eager"
options.add_argument("--headless=new")

pages: list[str] = []
threads: list[threading.Thread] = []
batch_size = 10
data = {}
num_pages = 0
progress = 0

with open("pages.json") as file:
    pages_to_scrape: list[str] = json.load(file)
    for page in pages_to_scrape:
        character_name = page.split("/")[-1]
        pages.append(page)
        pages.append(page + "/Story")
        data[character_name] = {}
    num_pages = len(pages)

def find_cell(driver: WebDriver, info_type: str, tag_name) -> WebElement | None:
    try:
        return driver.find_element(By.CSS_SELECTOR, f"[data-source={info_type}]").find_element(By.TAG_NAME, tag_name)
    except NoSuchElementException:
        return None
    
def parse_story(page: str):
    url_parts = page.split("/")
    character_name = str(url_parts[-2])

    driver = webdriver.Firefox(options=options)
    driver.get(page)

    story_items: list[str] = [
        f"[data-image-key='{character_name}_Item_1.png']", 
        f"[data-image-key='{character_name}_Item_2.png']",
        f"[data-image-key='{character_name}_Item_3.png']"
    ]

    try:
        scroll_to(driver, driver.find_element(By.CSS_SELECTOR, story_items[0]))
    except NoSuchElementException:
        print(f"could not find story item 1 for {page}")
        driver.quit()
        return

    story_item_urls = []

    for item in story_items:
        try:
            element = driver.find_element(By.CSS_SELECTOR, item)
            image = get_lazy_loaded_img(element, "src")
            story_item_urls.append(image)
        except NoSuchElementException:
            print(f"no element with {item} on {page}")

    data[character_name]["items"] = story_item_urls
    driver.quit()

def parse_cover(page: str):
    url_parts = page.split("/")
    character_name = str(url_parts[-1])

    driver = webdriver.Firefox(options=options)
    driver.get(page)

    cover_info = ["proportions", "medium", "fragrance", "inspo", "signature"]
    tag_names = ["div", "div", "div", "div", "a"]
    output_fields = ["dimensions", "medium", "fragrance", "inspiration", "signature"]
    cells = [find_cell(driver, cover_info[i], tag_names[i]) for i in range(len(cover_info))]
    
    for i, cell in enumerate(cells):
        field = output_fields[i]
        # If cell is none, we have an error. Print the error
        if cell is None:
            print(f"failed to get {field} for ${page}")
        # Signature requires special handling because it is an img
        elif field == "signature":
            data[character_name][field] = get_lazy_loaded_img(cell, "href")
        # All other fields can be found in innerHTML
        else:
            data[character_name][field] = cell.get_attribute("innerHTML")

    driver.quit()

def parse_page(page):
    url_parts = page.split("/")
    if url_parts[-1] == "Story":
        parse_story(page)
    else:
        parse_cover(page)

def get_eta():
    global start
    global progress
    elapsed = time.time() - start
    time_per_page = elapsed / progress
    eta = time_per_page * (num_pages - progress)
    mins = eta // 60
    secs = eta % 60
    return f"{int(mins)}m{round(secs)}s"

def work():
    global progress
    if len(pages) <= 0:
        return
        
    page = pages.pop()
    try:
        parse_page(page)
    except TimeoutError:
        print(f"timed out on {page}. Retrying")
        try:
            parse_page(page)
        except:
            print(f"retry failed for {page}. Aborting")
    except NoSuchWindowException:
        print(f"browsing context discarded. Retrying")
        try:
            parse_page(page)
        except:
            print(f"retry failed for {page}. Aborting")
    progress += 1
    print(f"{progress}/{num_pages} {get_eta()}" )
    work()

for i in range(batch_size):
    t = threading.Thread(target=work)
    threads.append(t)

start = time.time()
for t in threads:
    t.start()

for t in threads:
    t.join()

end = time.time()
print(end - start)

with open("data/profile.json", "w") as file:
    json.dump(data, file, indent=3)

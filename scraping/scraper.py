from threading import Thread
import time
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
import json

class Scraper:
    def __init__(self, output_path):
        self.pages: list[str] = []
        self.threads: list[Thread] = []
        self.data: dict = {}
        self.r1999_wiki = "https://reverse1999.fandom.com/wiki"
        self.options = Options()
        self.options.page_load_strategy = "eager"
        self.options.add_argument("--headless=new")
        self.output_path = output_path

    def get_pages_to_scrape(self, force_update = False):
        pass

    def scrape(self, num_threads = 10):
        self.start_time: int = 0
        self.progress = 0
        self.get_pages_to_scrape()
        self.num_pages = len(self.pages)

        for i in range(num_threads):
            t = Thread(target=self.work)
            self.threads.append(t)

        start = time.time()
        for t in self.threads:
            t.start()

        for t in self.threads:
            t.join()

        end = time.time()
        print(end - start)

        with open(self.output_path, "w") as file:
            # print(self.data)
            json.dump(self.data, file, indent=4)

    def get_eta(self):
        elapsed = time.time() - self.start_time
        time_per_page = elapsed / self.progress
        eta = time_per_page * (self.num_pages - self.progress)
        mins = eta // 60
        secs = eta % 60
        return f"{int(mins)}m{round(secs)}s"

    def work(self):
        if len(self.pages) <= 0:
            return
            
        page = self.pages.pop()
        try:
            self.parse_page(page)
        except TimeoutError:
            print(f"timed out on {page}. Retrying")
            try:
                self.parse_page(page)
            except:
                print(f"retry failed for {page}. Aborting")
        except NoSuchWindowException:
            print(f"browsing context discarded. Retrying")
            try:
                self.parse_page(page)
            except:
                print(f"retry failed for {page}. Aborting")
        self.progress += 1
        print(f"{self.progress}/{self.num_pages} {self.get_eta()}" )
        self.work()

    def parse_page(self, page):
        pass 

    # I want to use eager load strategy, but it sometimes means I don't get links to lazy loaded images. This functions helps solve the issue
    @staticmethod
    def get_lazy_loaded_img(cell: WebElement, attribute):
        image = cell.get_attribute(attribute)
        while not str(image).startswith("https"):
            time.sleep(0.1)
            image = cell.get_attribute(attribute)

        if type(image) is str:
            image = image.split(".png")[0] + ".png"
        return image

    # only chrome has a built in scrollTo function in selenium, but all browsers can replicate the effect with JS
    @staticmethod
    def scroll_to(driver: WebDriver, element: WebElement):
        driver.execute_script("arguments[0].scrollIntoView()", element)
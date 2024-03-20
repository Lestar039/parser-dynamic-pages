import contextlib
import time

import lxml.html as LH
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.options import Options
from lxml.html.clean import Cleaner


class CustomCleaner(Cleaner):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.safe_attrs_only = False
        self.kill_tags = ['script', 'noscript', 'style', 'footer', 'header', 'nav']


def get_text_from_url(url: str) -> str:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    with contextlib.closing(webdriver.Chrome(options=chrome_options)) as browser:
        browser.get(url)

        # download full page
        screen_height = browser.execute_script("return window.screen.height;")
        counter = 1
        while True:
            browser.execute_script("window.scrollTo(0, {0}*window.screen.height);".format(counter))
            time.sleep(1)
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == screen_height:
                break
            screen_height = new_height
            counter += 1

        # parse settings
        content = browser.page_source
        cleaner = CustomCleaner()
        content = cleaner.clean_html(content)
        doc = LH.fromstring(content)

        # parsing
        result = ""
        for elt in doc.iterdescendants():
            text = elt.text or ''
            tail = elt.tail or ''
            words = ' '.join((text, tail)).strip()
            if words:
                words = words.encode('utf-8')
                result = result + words.decode("utf-8") + '\n'
        return result


if __name__ == '__main__':
    print(get_text_from_url(url="https://www.trypplea.com"))

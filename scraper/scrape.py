from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import selenium.webdriver as webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from time import sleep
import json

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection

from scraper.utils import (
    has_integer_string, 
    is_coordinate_line,
    is_phone_number,
    remove_duplicates,
    state_abbreviation_map
)

CHROME_DRIVER_PATH = 'scraper/chromedriver.exe'
SBR_WEBDRIVER = 'https://brd-customer-hl_bad09b10-zone-scraping_browser1:f39cmp5li3ia@brd.superproxy.io:9515'

def scrape_website_local(website):
    print('Connecting to Selenium Browser...')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)
    wait = WebDriverWait(driver, 10)
    parsed_content = {}

    try:
        driver.get(website)
        print("Page loaded")
        locations = get_location_elements(driver)
        area_ids = [location.get_attribute('data-area-id') for location in locations]
        area_ids = remove_duplicates(area_ids)
        area_ids = [state for state in area_ids if state in state_abbreviation_map()]

        for index, area in enumerate(area_ids):
            location = driver.find_element(By.XPATH, f"//div[@data-area-id='{area}']")
            # Scroll into view and ignore empty categories
            if (location.location_once_scrolled_into_view):
                if (has_integer_string(location.text)):
                    print(f"Location {location.text} is in view")
                    location.click()
                    print(f"Location {location.text} has been clicked")
                    sleep(2)
                    print(f"Getting locations html content for {area}")
                    html = get_locations_content(driver, wait)
                    body_content = clean_body_content(html)
                    parsed_content[area] = split_on_phone(body_content)
        print("Finished parsing URL: Result: ") 
        return parsed_content
    finally:
        driver.quit()

def get_locations_content(driver: webdriver, wait: WebDriverWait):
    try:
        el = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'locations-list')))
        return el.get_attribute('innerHTML')
    except TimeoutException:
        print("Element not found")
        return ''

def get_location_elements(driver: webdriver):
    location_item = driver.find_element(By.CLASS_NAME, 'view-content')
    child_locations = location_item.find_elements(By.XPATH, "//div[@data-area-id]")
    return child_locations

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ''

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')
    for script_or_style in soup(['script', 'style']):
        script_or_style.extract()
    cleaned_content = soup.get_text(separator='\n')
    cleaned_content = '\n'.join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    return cleaned_content


def split_on_coordinates(dom_content):
    lines = dom_content.splitlines()
    blocks = []
    current_block = ""

    for line in lines:
        if is_coordinate_line(line):
            blocks.append(current_block.strip() + "\n")
            current_block = line + "\n"
        else:
            current_block += line + "\n"
    if current_block:
        blocks.append(current_block.strip() + "\n")

    return blocks

def split_on_phone(body_content):
    lines = body_content.splitlines()
    blocks = []
    current_block = ""

    for line in lines:
        if is_phone_number(line):
            if (current_block == ""):
                blocks[-1] = blocks[-1] + line + "\n"
            else:
                current_block += line + "\n"
                blocks.append(current_block.strip() + "\n")
                current_block = ""
        else:
            current_block += line + "\n"
    
    return blocks

#   Using BrightData Scraping Browser
#
# def scrape_website_remote(website):
#     sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')

#     with Remote(sbr_connection, options=ChromeOptions()) as driver:
#         print('Connected! Navigating...')
#         driver.get(website)
#         print('Taking   screenshot to file page.png')
#         driver.get_screenshot_as_file('./page.png')
#         print('Navigated! Scraping page content...')
#         html = driver.page_source
#         return html

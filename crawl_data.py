from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

driver = webdriver.Chrome("chromedriver")
url = "https://shopee.vn/Ch%C4%83m-s%C3%B3c-da-cat.160.2341"

driver.get(url)
time.sleep(5)
driver.find_ele

# if __name__ == "__main__":

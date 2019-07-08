from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from urllib.parse import quote
from pyquery import PyQuery as pq
from lxml import etree
import json

def index_page(page):
    try:
        url = "https://search.jd.com/Search?keyword=" + quote(KEYWORD)
        browser.get(url)
        if page > 1:
            input = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='p-skip']/input")))
            submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='p-skip']/a")))
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".gl-item")))
        get_products()
    except TimeoutException:
        #index_page(page)
        pass
            
def get_products():
    html = browser.page_source
    html = etree.HTML(html)
    items = html.xpath("//li[@class='gl-item']")
    res = []
    for item in items:
        img = item.xpath("./div/div[@class='p-img']/a/img/@src")
        if len(img) == 0:
            img = item.xpath("./div/div[@class='p-img']/a/img/@data-lazy-img")
        product = {
            "titel": ''.join(item.xpath("./div/div[@class='p-name p-name-type-2']/a/em/text()")),
            "price": item.xpath("./div/div[@class='p-price']/strong/i/text()")[0],
            "commit": item.xpath("./div/div[@class='p-commit']/strong/a/text()")[0],
            "shop": item.xpath("./div/div[@class='p-shop']/span/a/text()")[0],
            #"image": img[0]
        }
        res.append(product)
        #print(product, file=fout)
    save_to_file(res)
        
def save_to_file(res):
    with open(r"1.txt", "w") as fout:
        print(json.dumps({"data": res}, ensure_ascii=False), file=fout)
    
def main(MAX_PAGE=10):
    for i in range(MAX_PAGE + 1):
        index_page(i)
    browser.quit()
        
if __name__ == "__main__":
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, 10)
    KEYWORD = "iPad"
    main(1)

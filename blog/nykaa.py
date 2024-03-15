

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import psycopg2
from database import engine as en
from sqlalchemy import text


engine = en.connect()
def initialize_driver():
    options = Options()
    # options.headless =True
    # options.add_argument('--headless=new') 
    return webdriver.Chrome(options=options)

def get_products(driver, url, n):
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)

    products_dict = []
    scrollHeight = 0
    i = 1
    while i <= (10 * n):
        new_scrollHeight = driver.execute_script(f"window.scrollTo({scrollHeight}, ({scrollHeight}+(485)));return document.body.scrollHeight")
        time.sleep(1)

        i += 1
        products_list = driver.find_elements(By.CLASS_NAME, "css-1t10dtm")


        for product in products_list:
            product_id = product.get_attribute("href").split("/")[-1]
            product_title = product.find_element(By.CLASS_NAME, "css-ham81y").text
            product_description = product.find_element(By.CLASS_NAME, "css-8ncoj4").text
            product_link = product.get_attribute("href")
            product_price = product.find_element(By.CLASS_NAME, "css-1ijk06y").text

            # Store the data as a dictionary
            product_info = {
                "product_id": product_id,
                "name": product_title,
                "description": product_description,
                "price": product_price,
                "link": product_link
            }

            # products_dict[product_id] = product_info
            products_dict.append(product_info)

        time.sleep(1)
        if new_scrollHeight == scrollHeight:
            break
        scrollHeight += 485
        time.sleep(1)
    return products_dict

# def connect_to_db():
#     return psycopg2.connect(url)

def create_products_table():
    engine.execute(text('''
        DROP TABLE IF EXISTS products    
    '''))

    engine.execute(text("""
        CREATE TABLE IF NOT EXISTS products (
            product_id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255),
            description TEXT,
            price VARCHAR(50),
            link TEXT
        )
    """))

def insert_data_into_db(products_dict):
    for row in products_dict:
        row_dict = dict(row)
        engine.execute(
            text("""
                INSERT INTO products (product_id, name, description, price, link)
                VALUES (:product_id, :name, :description, :price, :link)
                ON CONFLICT (product_id) DO NOTHING
            """),
            row_dict
        )

n = int(input("Enter the no. of pages : "))

driver = initialize_driver()
products_dict = get_products(driver, "https://www.nykaafashion.com/catalogsearch/result/?q=Jeans+for+Men&utm_source=nykaabeauty&utm_medium=search_redirection&utm_campaign=frombeautyweb&search_redirection=True&p=1", n)

# fastdb = get_fastdb()

create_products_table()
insert_data_into_db(products_dict)

engine.commit()
engine.close()

driver.quit()
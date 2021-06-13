from os import name
from bs4 import BeautifulSoup
from numpy.core.fromnumeric import product
import pandas as pd
import requests
import json
import csv
import numpy as np

product_in_page_url = "https://shopee.vn/api/v4/search/search_items?by=relevancy&limit=50&match_id=2341&newest={}&order=desc&page_type=search&scenario=PAGE_OTHERS&version=2"
rating_url = "https://shopee.vn/api/v2/item/get_ratings?filter=0&flag=1&itemid={}&limit=6&offset={}&shopid={}&type=0"

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
           'x-requested-with': 'XMLHttpRequest'}


def check_status(reponse):
    print("Status code: {}".format(reponse.status_code), end=" ")
    check = True
    if (reponse.status_code != 200):
        check = False
        print("-> Fail")
    else:
        print("-> OK")
    return check


def crawl_product(n_begin, n_end):
    product_attr = []
    product_id, shop_id, name, brand = [], [], [], []
    view_count, shop_location, sold, price = [], [], [], []
    variations, rating_star, rating_count = [], [], []

    # Crawl products from 1-N_page
    for i, key in enumerate(range(n_begin-1, (n_end-1)*50+1, 50)):
        print("Crawl page: ", i+1)
        reponse = requests.get(
            product_in_page_url.format(key), headers=headers)
        if (check_status(reponse) != True):
            break
        product_items = json.loads(reponse.text)["items"]

        # Get item from product in page i_th
        for j in range(50):
            print("\tCrawl {}_th product in page {}!->OK".format(j, i+1))
            item_basic = product_items[j]["item_basic"]
            product_id.append(item_basic["itemid"])
            shop_id.append(item_basic["shopid"])
            name.append(item_basic["name"])
            variations.append(item_basic["tier_variations"][0]["options"])
            brand.append(item_basic["brand"])
            view_count.append(item_basic["view_count"])
            shop_location.append(item_basic["shop_location"])
            sold.append(item_basic["sold"])
            price.append([item_basic["price_min"], item_basic["price_max"]])
            rating_star.append(item_basic["item_rating"]["rating_star"])
            rating_count.append(
                item_basic["item_rating"]["rating_count"][1:-1])

    col = ["itemid", "shopid", "name", "variations", "brand", "shop_location",
           "view_count", "sold", "rating_star", "rating_count(1* - 5*)", "price"]
    product_attr = zip(product_id, shop_id, name, variations, brand, shop_location,
                       view_count, sold, rating_star, rating_count, price)
    products = pd.DataFrame(list(product_attr), columns=col)

    return products


def crawl_rating(itemid, shopid):

    reponse = requests.get(rating_url.format(
        itemid, 0, shopid), headers=headers)

    check_status(reponse)

    rating_total = json.loads(reponse.text)[
        "data"]["item_rating_summary"]["rating_total"]

    rating_star, comment, variations, price = [], [], [], [], []

    for i in range(0, int(rating_total/6) + 1, 6):
        reponse = requests.get(rating_url.format(
            itemid, i, shopid), headers=headers)
        print("\tCrawl comments in page {}!".format(i), end=" ")
        if (check_status(reponse) != True):
            break

        for j in range(6):
            rating_items = json.loads(reponse.text)["data"]["ratings"][j]
            rating_star.append(rating_items["rating_star"])
            comment.append(rating_items["comment"])
            product_items = rating_items["product_items"]
            sub_variation, sub_price = [], []
            for k in range(len(product_items)):
                sub_variation.append(product_items[k]["model_name"])
                sub_price.append(product_items[k]["price"])
            variations.append(sub_variation)
            price.append(sub_price)

    col = ["variations", "price", "rating_star", "comment"]
    ratings_cmt = pd.DataFrame(data=list(
        zip(variations, price, rating_star, comment)), columns=col)
    file_name = "{},{}.csv".format(itemid, shopid)
    ratings_cmt.to_csv("./cmt_ratings/{}".format(file_name), index=False)


if __name__ == "__main__":
    print("PLEASE READ README.md TO CRAWL CORRECTLY PAGE NUMBER!!!")
    # n_begin = int(input("Enter the first page: "))
    # n_end = int(input("Enter the last page: "))
    # products = crawl_product(n_begin, n_end)
    # products.to_csv("products.csv", index=False)

    n_b = int(input("Enter the first product: "))
    n_e = int(input("Enter the last product: "))
    products = pd.read_csv("products.csv")
    itemid = products["itemid"].to_numpy()
    shopid = products["shopid"].to_numpy()
    name = products["name"].to_numpy()
    for i in range(n_b, n_e+1):
        print(i, name[i])
        crawl_rating(itemid[i], shopid[i])
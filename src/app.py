__author__ = 'mark.tattersall'

import requests
import socket
from bs4 import BeautifulSoup

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}

request = requests.get("https://amazon.co.uk/Philips-Ambiance-Wireless-Lighting-Starter/dp/B01K1WP7Z4/ref=sr_1_5?s=lighting&ie=UTF8&qid=1483999019&sr=1-5",headers=headers)
content = request.content
soup = BeautifulSoup(content, "html.parser")
element = soup.find("span", {"id": "priceblock_ourprice", "class": "a-size-medium a-color-price"})
string_price = element.text.strip() # "149.99"

starting_price = 200

price_without_symbol = float(string_price[1:])

if price_without_symbol < starting_price:
    percentage_price_decrease = (1 - (price_without_symbol/starting_price)) * 100

    print("price decreased by {} %".format(str(percentage_price_decrease)))

#<span id="priceblock_ourprice" class="a-size-medium a-color-price">£49.99</span>
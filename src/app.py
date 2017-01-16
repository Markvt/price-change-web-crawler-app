__author__ = 'mark.tattersall'

import requests
import schedule
import time
import smtplib
from email.mime.text import MIMEText
import socket
from bs4 import BeautifulSoup

class Crawler:

    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }

    products_for_watch = [{
        "url": "https://amazon.co.uk/Philips-Ambiance-Wireless-Lighting-Starter/dp/B01K1WP7Z4/ref=sr_1_5?s=lighting&ie=UTF8&qid=1483999019&sr=1-5",
        "startingPrice": 149.99,
        "to": ["mark.tattersall@gmail.com"]
    }]

    def crawl(self):
        messages = []
        for product in self.products_for_watch:
            product_url = product.get("url")
            request = requests.get(product_url,headers=self.headers)
            content = request.content
            soup = BeautifulSoup(content, "html.parser")
            element = soup.find("span", {"id": "priceblock_ourprice", "class": "a-size-medium a-color-price"})
            string_price = element.text.strip() # "149.99"

            starting_price = product.get("startingPrice")

            price_without_symbol = float(string_price[1:])
            message = ""
            if price_without_symbol < starting_price:
                percentage_price_decrease = (1 - (price_without_symbol/starting_price)) * 100
                message = "price decreased by {} % for product {}".format(str(percentage_price_decrease), product_url)
                print(message)

            else:
                message = "There were no price decreases today for product :"  + str(product_url)
                print(message)
            messages.append(message + '\r\n')

            email_message = ", ".join(messages)
            for email_address in product.get("to"):
                to_address = email_address
                self.send_email(to_address, email_message)

    #<span id="priceblock_ourprice" class="a-size-medium a-color-price">£49.99</span>

    def send_email(self, to_address, message):
        from_address = "markvtattersall@hotmail.com"
        pwd = 'shee2Fon'
        to_address = "mark.tattersall@gmail.com"

        server = smtplib.SMTP("smtp.live.com",587)
        server.ehlo()
        server.starttls()
        server.ehlo
        server.login(from_address, pwd)
        server.set_debuglevel(1)
        msg = MIMEText(message)
        sender = from_address
        recipients = [to_address]
        msg['Subject'] = "crawler price alerts"
        msg['From'] = sender
        msg['To'] = ", ".join(recipients)
        server.sendmail(sender, recipients, msg.as_string())

    def run(self):
        #self.crawl()
        schedule.every().day.at("08:00").do(self.crawl,'It is 08:00')

        while True:
            schedule.run_pending()
            time.sleep(60)


if __name__ == "__main__" :
    crawler = Crawler()
    crawler.run()
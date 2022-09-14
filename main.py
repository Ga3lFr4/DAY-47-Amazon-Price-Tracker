import requests
import smtplib
from bs4 import BeautifulSoup
import lxml
from dotenv import load_dotenv
import os

load_dotenv("variables.env")

AMAZON_ENDPOINT = "https://www.amazon.fr/Logitech-LIGHTSYNC-clavier-m%C3%A9canique-switchs/dp/B07W5JKKX9/ref=sr_1_10?crid=2UQW7K9OPMPKK&keywords=clavier+gamer+logitech&qid=1663138147&sprefix=clavier+gamer%2Caps%2C99&sr=8-10"
header = {
    "Request Line": "GET / HTTP/1.1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.8",
}

TARGET_PRICE = 70

from_addr = os.getenv('FROM_ADDR')
password = os.getenv('PASSWORD')
my_email= os.getenv('MY_EMAIL')


response = requests.get(AMAZON_ENDPOINT, headers=header)
response.raise_for_status()
data = response.text

soup = BeautifulSoup(data, "lxml")
price_full = soup.find(name="span", class_="a-offscreen").getText()

price_without_symbol = price_full.replace(",", ".")[:-1]
float_price = float(price_without_symbol)


if float_price <= TARGET_PRICE:
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=from_addr, password=password)
        connection.sendmail(from_addr=from_addr, to_addrs=my_email, msg="Subject:Price Alert!\n\n"
                                                                                          f"Price low for your article, only {price_without_symbol}, shop now!\n{AMAZON_ENDPOINT}")

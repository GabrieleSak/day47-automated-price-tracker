import smtplib
import requests
from bs4 import BeautifulSoup
import lxml
from auth import *

URL = "https://www.amazon.de/-/en/dp/B08N2QK2TG/ref=gw_de_exp_desk_other_sc_eink_mlbp?pf_rd_r=SA27ZTH0QV62ZTWKHXXC&pf_rd_p=79dacdbe-da36-4c7b-aa81-382717768b3f&pd_rd_r=660bcaf1-96a3-4b71-8d6b-9e51ab4454f1&pd_rd_w=5AndH&pd_rd_wg=yodMJ&ref_=pd_gw_unk&th=1"
TARGET_PRICE = 190

response = requests.get(URL, headers={'Accept-Language': 'en-US,en;q=0.9',
                                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'})

product_web_page = response.text

soup = BeautifulSoup(product_web_page, "lxml")

product_name = soup.find(id="productTitle").getText()
print(product_name)

price_whole = soup.find(name="span", class_='a-price-whole').getText()
price_fraction = soup.find(name="span", class_='a-price-fraction').getText()
price = float(price_whole + price_fraction)

print(price)

if price <= TARGET_PRICE:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=email,
            msg=f"Subject:Amazon Price Alert!\n\n {product_name} is now €{price}\n{URL}".encode(
                "utf-8")
        )

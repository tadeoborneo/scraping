import requests
import sys
import csv
from bs4 import BeautifulSoup
from datetime import datetime
    
url = sys.argv[1] if len(sys.argv) > 1 else input("Enter a fravega item url: ")

def main():

    soup = BeautifulSoup(get_html(url),"html.parser")

    price = get_price(soup)
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("prices.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date,url,price])
    print(f"Saved: {date}, {price}")

def get_html(url):
    response = requests.get(url)
    if not response.ok:
        print(f"Unable to connect : {response.status_code}")
        exit()
    return response.text

def get_price(soup):
    price_span = soup.select_one(".sc-1d9b1d9e-0")
    
    if price_span:
        return price_span.text.strip()
    print("Unable to find price")
    exit()

main()
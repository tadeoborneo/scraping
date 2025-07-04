import requests
import sys
import csv
import os
from bs4 import BeautifulSoup
from datetime import datetime
    
url = sys.argv[1] if len(sys.argv) > 1 else input("Enter a fravega item url: ")
csv_file = "prices.csv"

def main():

    soup = BeautifulSoup(get_html(url),"html.parser")

    price = get_price(soup)
    num_price = clean_price(price)
    last_price = get_last_price(url,csv_file)
    last_price_num = clean_price(last_price) if last_price else None
    if last_price_num is not None:        
        if num_price == last_price_num:
            state = "No changes"
        elif num_price > last_price_num:
            state = "Higher price"
        else:
            state = "Lower price"
    else:
        state = "First log"

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not os.path.exists(csv_file):
        with open(csv_file,"w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "URL", "Price", "State"])

    with open("prices.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date,url,price,state])
    print(f"Saved: {date}, {price}")




def clean_price(price_str):
    return float(price_str.replace("$","").replace(".","").replace(",","."))

def get_last_price(url,csv_f):
    try:
        with open(csv_f,"r") as f:
            reader = csv.reader(f)
            prices = [row for row in reader if row[1] == url]
            if prices:
                return prices[-1][2]
    except FileNotFoundError:
        return None


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
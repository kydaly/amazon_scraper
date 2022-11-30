import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from time import sleep
import alerts

#needed to use the get function from the requests module
# User-Agent lets the server know what web browser you are using
# search commen user agent list on google to find what you need to put after the colon
# the one used here is for google chrome
Headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


def price_finder(interval=1):
    """This function reads in an excel file using pandas to get 3 necessary parameters. These include
    1) url for product, 2) name of the product and 3) the price to buy at. The function then uses requests
    and BeatifulSoup to get html content from the url. It then enters a for loop to extract the name of the
    item and price that it is listed at. If the price is below or equal to the value that is listed in the
    excel document."""

    # reciever is device that is recieving the notification
    reciever = '6263672354@vzwpix.com'
    # reads in data from an excel file and stores it as a dataframe
    item_tracker = pd.read_excel('Amazon_scraper.xlsx', 'Sheet1')
    # reads in columns under each name on spreadsheet (eg. url, code, price)
    # and stores them as a list from the dataframe
    item_tracker_URLS = item_tracker.url
    title = item_tracker.code
    buy_price = item_tracker.price  
    # loops using enumerate where x is used as the index (row) 
    # and url is each url link in each row of the excel sheet
    for x, url in enumerate(item_tracker_URLS):
      # uses Beautiful soup to get the html content from the webpage
        page = requests.get(url, headers=Headers)
        soup = BeautifulSoup(page.content, features="lxml")
        # gets the price as text by looking for the elements labeled as a span class
        # and a class=a-offscreen
        try:
            price = soup.find("span", attrs={"class":"a-offscreen"}).get_text()
            print("hi!")
        # exception if this is not found to print out a message saying the price
        # is not available
        except:
            price = ''
            print("Price is not available")
        # price is stored as a new variable and converted from text to a float
        num_price = price.replace('$', '')
        num_price = float(num_price)
        print(f"num_price is {num_price}")
        print(f"buy_price is {buy_price[x]}")
        # if the price from the site (num_price) is less than the price stored
        # in excel sheet (buy_price), an alert is sent to phone
        if num_price <= float(buy_price[x]):
          #calls separate alert function within alerts module
            alerts.alert(title[x],f'The price is {num_price}', reciever)
            
        # program pausees for 5 seconds before executing the next item (row) in the spreadsheet
        # used to avoid overloading the server
        sleep(5)
# calls function            
price_finder()

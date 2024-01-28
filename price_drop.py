import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import alerts

# needed to use the get function from the requests module
# User-Agent lets the server know what web browser you are using
# search commen user agent list on google to find what you need to put after the colon
# the one used here is for google chrome
Headers = {'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) (X11; Ubuntu; Linux x86_64; rv:78.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5',
            'Referer': 'https://google.com',
            'DNT': '1'
            }

def price_finder(interval=1):
    """This function reads in an excel file using pandas to get 3 necessary parameters. These include
    1) url for product, 2) name of the product and 3) the price to buy at. The function then uses requests
    and BeatifulSoup to get html content from the url. It then enters a for loop to extract the name of the
    item and price that it is listed at. If the price is below or equal to the value that is listed in the
    excel document."""

    # reciever is device that is recieving the notification
    # digitaltrends.com/mobile/how-to-send-a-text-from-your-email-account/
    # the above link shows the text after your phone number to put depending
    # on your carrier if you are located in the USA
    reciever = <phone_number+carrier_text>
    item_tracker = pd.read_excel('Amazon_scraper.xlsx', 'Sheet1')

    # reads in columns under each name on spreadsheet (eg. url, code, price)
    # and stores them as a list from the dataframe
    item_tracker_URLS = item_tracker.url
    title = item_tracker.code
    buy_price = item_tracker.price  
    for x, url in enumerate(item_tracker_URLS):

        # uses requests and BeautifulSoup to get the html content from the webpage
        page = requests.get(url, headers=Headers)
        soup = BeautifulSoup(page.content, "lxml")
        
        # gets the price as text from html content
        try:
            price = soup.find("span", class_="aok-offscreen").get_text()
            num_price = price.replace('$', '')
            num_price = float(num_price)
            print(f"num_price is {num_price}")

            # If price is lower than what is specified on the excel file a
            # notification is sent
            if num_price <= float(buy_price[x]):
                alerts.alert(title[x], f'The price is {num_price}', url, reciever)
        except:
            price = ''
            try:
                price = soup.find("span", class_="a-offscreen").get_text()
                num_price = price.replace('$', '')
                num_price = float(num_price)
                print(f"num_price is {num_price}")
                if num_price <= float(buy_price[x]):
                    alerts.alert(title[x], f'The price is {num_price}', url, reciever)
            except:
                price = ''
                print("Price is not available. Check website for HTML changes.")
                
        # program pausees for 5 seconds before executing the next item (row) in the spreadsheet
        # used to avoid overloading the server
        sleep(5)
            
price_finder()

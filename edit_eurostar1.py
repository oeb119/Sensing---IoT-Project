import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def get_time():
    # Get the current date and time
    current_time = datetime.now()
    # Format the time into "day_hour_minute"
    formatted_time = current_time.strftime("%d_%H_%M")
    return formatted_time

#formatted_time = get_time()

# print("RUNNING EDIT")

## CALLED Later to get URL
def get_url(origin, destination, date, day):
    """Generate a url from a search term"""
    template = "https://www.eurostar.com/search/uk-en?adult=1&origin={}&destination={}&outbound={}{}"
    origin= origin.replace(" ", "+")
    destination= destination.replace(" ", "+")
    date= date.replace(" ", "+")
    return template.format(origin, destination, date, day)

# day = 14
# url = get_url("7015400", "8727100", "2023-12-", str(day))

## Create web driver instance
def create_driver():
    driver = webdriver.Chrome()
    return driver

# driver = create_driver()

## Scrapes data
def scrape_data(driver, url):
    driver.get(url)
    # Explicitly wait for the cookies prompt to appear
    try:
        continue_without_accepting_link = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='continueWithoutAccepting']"))
        )
        # Click the "Continue without accepting" link
        continue_without_accepting_link.click()

    except Exception as e:
        print("Error:", e)
    
    # Initialize BeautifulSoup with the page content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

# soup = scrape_data(driver, url)

## CALLED Later to find/scrape train info in each train listing
def get_trains_listings(listing):
    """Extract trains listings information from the raw html"""

    try:
        #departure
        departure = listing.find("span", class_="css-108sy5j").text.replace("\n", "")
    except AttributeError:
        return "departure error"
        
    try:
        #price
        price = listing.find("span", class_="css-1a2zyvq").text.replace("\n", "")
    except AttributeError:
        return "price error"
    # NOW ITS: css-1a2zyvq
    # BEFORE NOV 30 IT WAS: css-pls0gd

    try:
        #duration
        time_element = listing.find("div", class_="css-cz93xk")
        text_elements = [span.text for span in time_element.find_all("span")]
        duration = ' '.join(text_elements)
    except AttributeError:
        return "duration error"

    trains_listings = (departure, price, duration)
    return trains_listings

## Makes a list of lists of train info
def trains_listings(soup):
    trains = []
    listings = soup.find_all("div", class_ = "MuiGrid2-root MuiGrid2-container MuiGrid2-direction-xs-row css-15w28yb")

    ## ONLY TO CREATE TRAINS VARIABLE
    for listing in listings:
        trains_lists = get_trains_listings(listing) #checks to see if what we return from the function is empty or not
        if trains_lists:
            trains.append(trains_lists) #if the trains_lists has something in it, then we would append that to the trains list.

    print(trains)
    return trains

# trains = trains_listings(soup)

## Makes CSV name
def get_csv_name(day, formatted_time):
    """Generate a url from a search term"""
    template = "eurostar_dec_{}_2023_at_{}.csv"
    return template.format(day, formatted_time)

# csv_name = get_csv_name(str(day), formatted_time)

## Puts the train list info in a dataframe and saves it in csv file
def dataframe(csv_name, trains):
    # Create an empty list to hold the data
    data_list = []

    # Iterate through the data and append to the list
    for item in trains:
        if isinstance(item, tuple) and len(item) == 3:
            data_list.append([item[0], item[1], item[2]])  # Use a list instead of a dictionary

    # Create a DataFrame from the list with column names
    df = pd.DataFrame(data_list, columns=['Time', 'Price', 'Description'])
    
    #Exporting the DataFrame as csv
    df.to_csv(csv_name, index=False, sep=";")
    return df

# df = dataframe(csv_name, trains)

# print(df)

## Returns price of cheapest train
def cheapest(df):
    print(df)
    if df.empty:
        return ""  # Return an empty string if df is not a DataFrame
    else:
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        min_price_row = df.loc[df['Price'].idxmin()]
        print(min_price_row)
        return min_price_row[1]

# cheapest_train = cheapest(df)

# print(cheapest_train)

def close_driver(driver):
    driver.quit()  # Close the provided WebDriver instance

# close_driver(driver)
"""Important libraries to install """
import csv
import time
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Add the locations here that you want to scrape events from desired countries
Total_locations = ['París', 'Barcelona', 'Birmingham', 'Valencia', 'Sevilla', 'Zaragoza', 'Málaga', 'Marsella',
                   'Lyon', 'Berlín', 'Hamburgo', 'Múnich', 'London', 'Manchester', 'Madrid']
HEADER_FILE = ['Event name', 'Ticket type', 'Event date', 'Nº tickets available', 'Nº tickets sold',
               'Nº tickets wanted',
               'Lower selling ticket price available ', 'Lower selling ticket price recently sold 1',
               'Lower selling ticket price recently sold 2',
               'Lower selling ticket price recently sold 3']
urls = list()
today = datetime.now()
tomorrow = today + timedelta(1)
OUTPUT_FILE_NAME = 'Data_' + time.strftime("%b %d %Y_ %I-%M-%S %p") + '.csv'


def configure_driver():
    # Add additional Options to the webdriver
    chrome_options = Options()
    # add the argument and make the browser Headless.
    # chrome_options.add_argument("--headless")  # if you don't want to see the display on chrome just uncomment this
    chrome_options.add_argument("--log-level=3")  # removes error/warning/info messages displayed on the console
    chrome_options.add_argument("--disable-notifications")  # disable notifications
    chrome_options.add_argument(
        "--disable-infobars")  # disable infobars ""Chrome is being controlled by automated test software"  Although is isn't supported by Chrome anymore
    chrome_options.add_argument("start-maximized")  # will  chrome screen
    # chrome_options.add_argument('--disable-gpu')  # disable gmaximizepu (not load pictures fully)
    chrome_options.add_argument("--disable-extensions")  # will disable developer mode extensions
    # chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    # chrome_options.add_argument('--proxy-server=%s' % PROXY)
    # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:8100")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=chrome_options)  # you don't have to download chromedriver it will be downloaded by itself and will be saved in cache
    return driver


def RunScrapper():
    start_time = time.time()
    urls1 = ["https://www.ticketswap.com/browse?location=510&period=today",
            "https://www.ticketswap.com/browse?location=552&period=today",
            "https://www.ticketswap.com/browse?location=1424&period=today",
            "https://www.ticketswap.com/browse?location=674&period=today",
            "https://www.ticketswap.com/browse?location=2159&period=today",
            "https://www.ticketswap.com/browse?location=2160&period=today",
            "https://www.ticketswap.com/browse?location=2629&period=today",
            "https://www.ticketswap.com/browse?location=586&period=today",
            "https://www.ticketswap.com/browse?location=572&period=today",
            "https://www.ticketswap.com/browse?location=2&period=today",
            "https://www.ticketswap.com/browse?location=17&period=today",
            "https://www.ticketswap.com/browse?location=334&period=today",
            "https://www.ticketswap.com/browse?location=542&period=today",
            "https://www.ticketswap.com/browse?location=515&period=today",
            "https://www.ticketswap.com/browse?location=545&period=today"]

    urls2 = ["https://www.ticketswap.com/browse?location=510", "https://www.ticketswap.com/browse?location=552",
            "https://www.ticketswap.com/browse?location=1424", "https://www.ticketswap.com/browse?location=674",
            "https://www.ticketswap.com/browse?location=2159", "https://www.ticketswap.com/browse?location=2160",
            "https://www.ticketswap.com/browse?location=2629", "https://www.ticketswap.com/browse?location=586",
            "https://www.ticketswap.com/browse?location=572", "https://www.ticketswap.com/browse?location=2",
            "https://www.ticketswap.com/browse?location=17", "https://www.ticketswap.com/browse?location=334",
            "https://www.ticketswap.com/browse?location=542", "https://www.ticketswap.com/browse?location=515",
            "https://www.ticketswap.com/browse?location=545"]

    # Click on the location
    while True:
        print("***********************************")
        print("1).Press 1 for only Today's Data.")
        print("2).Press 2 for Anytime Data.")
        choice = input()
        if choice == '1':
            Click_on_the_location(urls1)
            break
        elif choice == '2':
            Click_on_the_location(urls2)
            break
        print("Please enter the right choice!")

    print("time elapsed: {:.2f}s".format(time.time() - start_time))


# Click on the location
def Click_on_the_location(urls1):
    for url in urls1:
        # Get to the website
        driver.get(url)
        # # click on the location bar
        # driver.find_element(By.XPATH, value="//li[@class = 'css-s1x3f1 erc5tuo1']").click()
        # # Find the search bar
        # i = driver.find_element(By.XPATH, value="//input[@id = 'citysearch']")
        # # write the location into the search bar
        # i.send_keys(location)
        # # press to enter
        # i.send_keys(Keys.RETURN)
        # time.sleep(2)
        # Actual Location Modal
        # l = driver.find_element(By.XPATH, value="//div[@class ='css-xczmhq e1gsu8qn3']")
        # l.find_element(By.XPATH, value="//button[@class ='css-1gaplt1 e1gsu8qn4']").click()
        time.sleep(2)
        # Check for the cookies button
        try:
            driver.find_element(By.XPATH, value="//button[@class = 'css-853sc5 e1dvqv261']").click()
        except:
            pass
        # Get all the links of events
        Get_the_links()
        # Get into the events
        Get_into_the_events(urls)
        urls.clear()
        # print("***************************************")


# Get all the links of events
def Get_the_links():
    # grab the links if visible
    while True:
        try:
            WebDriverWait(driver, 5).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//a[@role]"))
            )
            ele = driver.find_element(By.XPATH, value="//button[@class = 'e1mdulau0 css-1qp2od eh8fd9012']")
            # create action chain object
            action = ActionChains(driver)
            # perform the operation
            action.move_to_element(ele).perform()
            driver.execute_script("arguments[0].click();", ele)
            WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//button[@class = 'e1mdulau0 css-1qp2od eh8fd9012']"))
            )
        except:
            break
    # Parse the  Html  using Bs4
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = soup.findAll('span', attrs={'class': 'pill css-1a10nyx e1pqc3131'})
    count = 1
    for link in links:
        link = link.findParent('a').get('href')
        # print(count, ":", link)
        urls.append(link)
        count += 1
    time.sleep(10)
    return urls


# Get into the events
def Get_into_the_events(urls):
    for link in urls:
        driver.get(link)
        # Parse the  Html  using Bs4
        soup = BeautifulSoup(driver.page_source, "html.parser")
        link_parents = soup.findAll('span', attrs={'class': 'pill css-1a10nyx e1pqc3131'})
        try:
            time.sleep(1)
            fans_also_like = bool(driver.find_element(By.XPATH, value="//h3[@class ='css-1cuhhbp e3uwxol0']"))
            if fans_also_like:
                time.sleep(0.5)
                continue
        except:
            pass

        # If the ticket type links are available then:
        if bool(link_parents):
            Ticket_type_links(link_parents)
        # If the ticket type links are not available then:
        else:
            Ticket_type_link_not_available(soup)
        time.sleep(0.5)


# If the ticket type links are available then:
def Ticket_type_links(link_parents):
    for link_parent in link_parents:
        # Ticket Type
        Ticket_type = link_parent.findParent('a').findChild('h4').text
        link = link_parent.findParent('a').get('href')
        driver.get(link)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # If wanted, available, sold doesn't exist
        try:
            check = bool(soup.findAll('span', attrs={'class': 'css-2tbp88 ewd9yqi2'}))
        except:
            check = True
        if not check:
            pass
        # If wanted, available, sold exist
        elif check:
            # Overall Data
            over_all_data = event(Ticket_type)
            OUTPUT_RESULT = over_all_data
            write_to_file([OUTPUT_RESULT])
            print("************************")


# if the ticket type link not available
def Ticket_type_link_not_available(soup):
    # soup = BeautifulSoup(driver.page_source, "html.parser")
    # If wanted, available, sold doesn't exist
    try:
        check = bool(soup.findAll('span', attrs={'class': 'css-2tbp88 ewd9yqi2'}))
    except:
        check = True
    if not check:
        pass
    # If wanted, available, sold exist
    elif check:
        # Overall Data
        over_all_data = event1()
        OUTPUT_RESULT = over_all_data
        write_to_file([OUTPUT_RESULT])
        print("************************")


# If the ticket type links are available then go to this function for scraping:
def event(Ticket_type):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    sold_low_price1 = 'No tickets have been sold so far.'
    sold_low_price2 = 'No tickets have been sold so far.'
    sold_low_price3 = 'No tickets have been sold so far.'
    # Event Name
    try:
        Event_Name = soup.find('div', attrs={'class': 'css-voqkl8 ej1og8q2'}).text
    except:
        Event_Name = ''
    # Event Date
    try:
        # Today date
        today = datetime.now()
        # Tomorrow Date
        tomorrow = today + timedelta(1)
        event_date = soup.find('p', attrs={'class': 'css-mcvk2t ej1og8q8'}).text
        # If date format is Tomorrow, 11:00 PM:
        if "Tomorrow" in event_date:
            confirm_date = tomorrow.strftime("%d/%m/%Y")

        # If date format is Today, 09:00 AM:
        elif "Today" in event_date:
            confirm_date = today.strftime("%d/%m/%Y")

        # If date format is Jan 22 – 25:
        elif '–' in event_date:
            confirm_date = event_date
        # If date format is Friday, Oct 6, 2023, 09:00 PM:
        else:
            event_date = datetime.strptime(event_date, "%A, %b %d, %Y, %I:%M %p")
            confirm_date = event_date.strftime("%d/%m/%Y")
    except:
        confirm_date = ''

    # if  date format is Saturday, Dec 31, 09:30 PM:
    try:
        event_date = soup.find('p', attrs={'class': 'css-mcvk2t ej1og8q8'}).text
        event_date = datetime.strptime(event_date, "%A, %b %d, %I:%M %p")
        confirm_date = event_date.strftime("%d/%m")
        confirm_date = confirm_date + '/' + str(today.year)
    except:
        pass

    # Available
    try:
        available = soup.findAll('span', attrs={'class': 'css-2tbp88 ewd9yqi2'})
        available = available[0].text
    except:
        available = ''

    # Sold
    try:
        sold = soup.findAll('span', attrs={'class': 'css-2tbp88 ewd9yqi2'})
        sold = sold[1].text
    except:
        sold = ''
    # Low Price Sold
    try:
        if sold != '0':
            WebDriverWait(driver, 2).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//div[@class='e1od3zle0 css-1njc5y4 eh8fd9012']//strong"))
            )
            sold_low_price = driver.find_elements(By.XPATH,
                                                  value="//div[@class='e1od3zle0 css-1njc5y4 eh8fd9012']//strong")
            sold_low_price1 = sold_low_price[0].text.strip("\n/ ticket")
            sold_low_price2 = sold_low_price[1].text.strip("\n/ ticket")
            sold_low_price3 = sold_low_price[2].text.strip("\n/ ticket")

    except:
        pass
    # Wanted
    try:
        wanted = soup.findAll('span', attrs={'class': 'css-2tbp88 ewd9yqi2'})
        wanted = wanted[2].text
    except:
        wanted = ''

    # Available low price
    try:
        available_low_price = soup.find('div', attrs={'class': 'e1asqgj30 css-19fqo0n eh8fd9012'}).find(
            'strong').text
        available_low_price = available_low_price.strip("/ ticket")
    except:
        available_low_price = ''
    over_all_data = [Event_Name] + [Ticket_type] + [confirm_date] + [available] + [sold] + [wanted] + [
        available_low_price] + [
                        sold_low_price1] + [
                        sold_low_price2] + [
                        sold_low_price3]
    print("✅Event Name:", Event_Name)
    print("✅Ticket Type:", Ticket_type)
    print("✅Event Date:", confirm_date)
    print("✅Available:", available)
    print("✅Sold:", sold)
    print("✅Wanted:", wanted)
    print("✅Available Low Price:", available_low_price)
    print("✅Low Sold Price1:", sold_low_price1)
    print("✅Low Sold Price2:", sold_low_price2)
    print("✅Low Sold Price3:", sold_low_price3)
    return over_all_data


# If the ticket type links are not available then go to this function for scraping:
def event1():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    sold_low_price1 = 'No tickets have been sold so far.'
    sold_low_price2 = 'No tickets have been sold so far.'
    sold_low_price3 = 'No tickets have been sold so far.'
    # Ticket Type
    try:
        Ticket_Type = soup.find('div', attrs={'class': 'css-fss94e evy9nty5'}).find('h2', attrs={
            'class': 'css-55f8c0 eloqthd4'}).text
    except:
        Ticket_Type = ''
    # Event Name
    try:
        Event_Name = soup.find('div', attrs={'class': 'css-voqkl8 ej1og8q2'}).text
    except:
        Event_Name = ''
    # Event Date
    try:
        # Today date
        today = datetime.now()
        # Tomorrow Date
        tomorrow = today + timedelta(1)
        event_date = soup.find('p', attrs={'class': 'css-mcvk2t ej1og8q8'}).text
        # If date format is Tomorrow, 11:00 PM:
        if "Tomorrow" in event_date:
            confirm_date = tomorrow.strftime("%d/%m/%Y")

        # If date format is Today, 09:00 AM:
        elif "Today" in event_date:
            confirm_date = today.strftime("%d/%m/%Y")

        # If date format is Jan 22 – 25:
        elif '–' in event_date:
            confirm_date = event_date

        # If date format is Friday, Oct 6, 2023, 09:00 PM:
        else:
            event_date = datetime.strptime(event_date, "%A, %b %d, %Y, %I:%M %p")
            confirm_date = event_date.strftime("%d/%m/%Y")
    except:
        confirm_date = ''

    # if  date format is Saturday, Dec 31, 09:30 PM:
    try:
        event_date = soup.find('p', attrs={'class': 'css-mcvk2t ej1og8q8'}).text
        event_date = datetime.strptime(event_date, "%A, %b %d, %I:%M %p")
        confirm_date = event_date.strftime("%d/%m")
        confirm_date = confirm_date + '/' + str(today.year)
    except:
        pass

    # Available
    try:
        available = soup.findAll('span', attrs={'class': 'css-2tbp88 ewd9yqi2'})
        available = available[0].text
    except:
        available = ''

    # Sold
    try:
        sold = soup.findAll('span', attrs={'class': 'css-2tbp88 ewd9yqi2'})
        sold = sold[1].text
    except:
        sold = ''
    # Low Price Sold
    try:
        if sold != '0':
            WebDriverWait(driver, 2).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, "//div[@class='e1od3zle0 css-1njc5y4 eh8fd9012']//strong"))
            )
            sold_low_price = driver.find_elements(By.XPATH,
                                                  value="//div[@class='e1od3zle0 css-1njc5y4 eh8fd9012']//strong")
            sold_low_price1 = sold_low_price[0].text.strip("\n/ ticket")
            sold_low_price2 = sold_low_price[1].text.strip("\n/ ticket")
            sold_low_price3 = sold_low_price[2].text.strip("\n/ ticket")

    except:
        pass
    # Wanted
    try:
        wanted = soup.findAll('span', attrs={'class': 'css-2tbp88 ewd9yqi2'})
        wanted = wanted[2].text
    except:
        wanted = ''

    # Available low price
    try:
        available_low_price = soup.find('div', attrs={'class': 'e1asqgj30 css-19fqo0n eh8fd9012'}).find(
            'strong').text
        available_low_price = available_low_price.strip("/ ticket")
    except:
        available_low_price = ''
    over_all_data = [Event_Name] + [Ticket_Type] + [confirm_date] + [available] + [sold] + [wanted] + [
        available_low_price] + [
                        sold_low_price1] + [
                        sold_low_price2] + [
                        sold_low_price3]
    print("✅Event Name:", Event_Name)
    print("✅Ticket Type:", Ticket_Type)
    print("✅Event Date:", confirm_date)
    print("✅Available:", available)
    print("✅Sold:", sold)
    print("✅Wanted:", wanted)
    print("✅Available Low Price:", available_low_price)
    print("✅Low Sold Price1:", sold_low_price1)
    print("✅Low Sold Price2:", sold_low_price2)
    print("✅Low Sold Price3:", sold_low_price3)
    return over_all_data


def write_to_file(rows):
    file = open(OUTPUT_FILE_NAME, 'a', encoding="utf-8-sig", newline="")
    writer = csv.writer(file)
    writer.writerows(rows)
    file.close()


if __name__ == "__main__":
    # create the driver object.
    driver = configure_driver()
    write_to_file([HEADER_FILE])
    # call the scrapper to run
    RunScrapper()
    # close the driver.
    # driver.close()

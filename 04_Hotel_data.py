import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.agoda.com/search?city=1390&checkIn=2024-04-25&los=5&rooms=1&adults=2&children=0&cid=1922890&locale=en-us&ckuid=d9119135-c09b-464f-a7f1-0d5227737dce&prid=0&gclid=Cj0KCQjwlZixBhCoARIsAIC745D0F2nj-A42FnxWN2ulWtuttxwxJTV7b-YjFO_XqXZwcyENify-Kp8aAtmoEALw_wcB&currency=USD&correlationId=fb00f692-f681-4e2b-a478-2c48f58a5355&analyticsSessionId=-372867373246697419&pageTypeId=1&realLanguageId=1&languageId=1&origin=BD&tag=56607b72-e9a1-472a-8654-4037959dedf1&userId=d9119135-c09b-464f-a7f1-0d5227737dce&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=7&currencyCode=USD&htmlLanguage=en-us&cultureInfoName=en-us&machineName=sg-pc-6g-acm-web-user-997bb7d77-fhk9n&trafficGroupId=5&sessionId=0kqxjjr1qrnagy0miuxf4jpw&trafficSubGroupId=122&aid=82361&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&browserFamily=Chrome&cdnDomain=agoda.net&checkOut=2024-04-30&priceCur=USD&textToSearch=Dhaka&travellerType=1&familyMode=off&ds=UFGAfKjLuRj6Q6fN&productType=-1")
# Wait for the page to load
time.sleep(5)

# Function to check if the next button is present
def is_next_button_present():
    try:
        driver.find_element(By.ID, "paginationNext")
        return True
    except NoSuchElementException:
        return False

# Find all hotel names, currencies, and prices on the first page
hotel_names = wait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3[data-selenium='hotel-name']")))
hotel_currencies = wait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[data-selenium='hotel-currency']")))
hotel_prices = wait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[data-selenium='display-price']")))
hotel_properties = wait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-selenium='pill-container']")))

while True:
    # Scroll down to the last elements in the lists
    driver.execute_script('arguments[0].scrollIntoView();', hotel_names[-1])
    driver.execute_script('arguments[0].scrollIntoView();', hotel_currencies[-1])
    driver.execute_script('arguments[0].scrollIntoView();', hotel_prices[-1])
    driver.execute_script('arguments[0].scrollIntoView();', hotel_properties[-1])
    try:
        # Wait for more elements to be loaded
        wait(driver, 30).until(lambda driver: len(wait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3[data-selenium='hotel-name']")))) > len(hotel_names))
        wait(driver, 30).until(lambda driver: len(wait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[data-selenium='hotel-currency']")))) > len(hotel_currencies))
        wait(driver, 30).until(lambda driver: len(wait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[data-selenium='display-price']")))) > len(hotel_prices))
        wait(driver, 30).until(lambda driver: len(wait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-selenium='pill-container']")))) > len(hotel_properties))
        # Update lists
        if driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='display-price']") == None:
            continue
        hotel_names = driver.find_elements(By.CSS_SELECTOR, "h3[data-selenium='hotel-name']")
        hotel_currencies = driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='hotel-currency']")
        hotel_prices = driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='display-price']")
        hotel_properties = driver.find_elements(By.CSS_SELECTOR, "div[data-selenium='pill-container']")
        
    except:
        # Break the loop if no new elements are loaded after scrolling
        break

# Write data to CSV
with open('dhaka_hotel.csv', 'w') as f:
    for hotel_name, hotel_currency, display_price, pill_container in zip(hotel_names, hotel_currencies, hotel_prices, hotel_properties):
        line = f"{hotel_name.text},{hotel_currency.text},{display_price.text},{pill_container.text.strip().replace('\n', ' | ')}\n"
        f.write(line)

# Pagination - locate and click on the next page button if available
while is_next_button_present():
    next_button = driver.find_element(By.ID, "paginationNext")
    driver.execute_script("arguments[0].click();", next_button)  # Click using JavaScript
    time.sleep(5)  # Let the new page load
    
    # Refresh elements
    hotel_names = driver.find_elements(By.CSS_SELECTOR, "h3[data-selenium='hotel-name']")
    hotel_currencies = driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='hotel-currency']")
    hotel_prices = driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='display-price']")
    hotel_properties = driver.find_elements(By.CSS_SELECTOR, "div[data-selenium='pill-container']")
    while True:
        # Scroll down to last elements in lists
        driver.execute_script('arguments[0].scrollIntoView();', hotel_names[-1])
        driver.execute_script('arguments[0].scrollIntoView();', hotel_currencies[-1])
        driver.execute_script('arguments[0].scrollIntoView();', hotel_prices[-1])
        driver.execute_script('arguments[0].scrollIntoView();', hotel_properties[-1])
        try:
            # Wait for more elements to be loaded
            wait(driver, 30).until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "h3[data-selenium='hotel-name']")) > len(hotel_names))
            wait(driver, 30).until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='hotel-currency']")) > len(hotel_currencies))
            wait(driver, 30).until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='display-price']")) > len(hotel_prices))
            wait(driver, 30).until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR,  "div[data-selenium='pill-container']")) > len(hotel_properties))
            # Update lists
            hotel_names = driver.find_elements(By.CSS_SELECTOR, "h3[data-selenium='hotel-name']")
            hotel_currencies = driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='hotel-currency']")
            hotel_prices = driver.find_elements(By.CSS_SELECTOR, "span[data-selenium='display-price']")
            hotel_properties = driver.find_elements(By.CSS_SELECTOR, "div[data-selenium='pill-container']")
        except:
            # Break the loop if no new elements are loaded after scrolling
            break

driver.quit()
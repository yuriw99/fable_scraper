import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import random

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def convert_to_date(relative_text):
    # Get the current date
    current_date = datetime.now()
    
    # Split the input to get the number and the time unit
    amount, unit = relative_text.split()[:2]
    amount = int(amount)  # Convert the number part to an integer

    random_day = random.randint(1, 28)

    # Calculate the date based on the unit
    if 'month' in unit:
        new_date = current_date - relativedelta(months=amount)
    elif 'year' in unit:
        new_date = current_date - relativedelta(years=amount)
    elif 'week' in unit:
        new_date = current_date - timedelta(weeks=amount)
    else:
        raise ValueError("Unsupported time unit.")
    new_date = new_date.replace(day=random_day)
    # Format the date as dd/mm/yyyy
    return new_date.strftime('%d/%m/%Y')



review_data = []

def getReviews(fable_URL, product_URL, id, handle, times):
    driver = webdriver.Chrome()

    driver.get(fable_URL)


    for x in range(times):
        try:
            # Check and close the ad button if it exists
            ad_close_buttons = driver.find_elements(By.XPATH, '//button[contains(@class, "needsclick")]')
            if ad_close_buttons:
                ad_close_buttons[0].click()
                time.sleep(1)  # Small delay to ensure ad is closed
            
            # Wait for the "Show More" button to be clickable and click it
            show_more_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "oke-showMore-button")]'))
            )
            driver.execute_script("arguments[0].click();", show_more_link)  # Use JavaScript click
            time.sleep(2)
        except Exception as e:
            print("No more 'Show More' button found or an error occurred:", e)
            break

    page_source = driver.page_source
    driver.quit()



    soup = BeautifulSoup(page_source, 'html.parser')

    reviews = soup.find_all('li', class_='oke-w-reviews-list-item')  


    for review in reviews:
        review_text = review.find('div', class_='oke-reviewContent-body').get_text(strip=True)
        filled_stars = review.find('span', class_='oke-a11yText')
        review_rating = filled_stars.get_text(strip=True)[6]  # Example class for ratings
        review_author = review.find('div', class_='oke-w-reviewer-identity').get_text(strip=True)  # Example class for author
        review_date = review.find('div', class_='oke-reviewContent-date').get_text(strip=True)
        review_title = review.find('div', class_='oke-reviewContent-title').get_text(strip=True)
        review_data.append({
                'title' : review_title,
                'body': review_text,
                'rating': review_rating,
                'review_date': convert_to_date(review_date),
                'reviewer_name': review_author,
                'reviewer_email': '',
                'product_url': product_URL,
                'picture_urls': '',
                'product_id': id,
                'product_handle': handle

            })
getReviews('https://fablepets.com/products/toy?_pos=1&_psq=falcon+&_ss=e&_v=1.0', 'https://www.puplist.co/products/falcon-toy', '7701056127038', 'falcon-toy', 30)
print(len(review_data))
getReviews('https://fablepets.com/products/signature-ball?_pos=2&_psq=signture+b&_ss=e&_v=1.0', 'https://www.puplist.co/products/signature-ball', '7701055832126', 'signature-ball', 3)
print(len(review_data))
getReviews('https://fablepets.com/products/bed-cover?_pos=2&_psq=b&_ss=e&_v=1.0', 'https://www.puplist.co/products/bed-cover', '7701056094270', 'bed-cover', 7)
print(len(review_data))
getReviews('https://fablepets.com/products/the-game?_pos=1&_psq=p&_ss=e&_v=1.0', 'https://www.puplist.co/products/the-puffin-A2-game', '7701056159806', 'the-puffin™-game', 45)
print(len(review_data))
getReviews('https://fablepets.com/products/armadillo?_pos=1&_psq=ar&_ss=e&_v=1.0', 'https://www.puplist.co/products/armadillo', '7701055701054', 'armadillo™', 7)
print(len(review_data))
getReviews('https://fablepets.com/products/twin-falcon-toy?_pos=2&_psq=t&_ss=e&_v=1.0', 'https://www.puplist.co/products/twin-falcon-toy', '7701056290878', 'twin-falcon-toy', 1)
df = pd.DataFrame(review_data)
df.to_csv('fable_reviews_3.csv', index=False)



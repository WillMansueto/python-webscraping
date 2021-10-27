import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep

#Preparing 
city = input('Where are you going? ')
options = Options()
options.add_argument('window-size=400,800')
browser = webdriver.Chrome(options=options)
browser.get('https://airbnb.com')
sleep(2)

#moving through the website
btn_query = browser.find_element(By.TAG_NAME, 'button')
btn_query.click()
sleep(0.5)
input_place = browser.find_element(By.NAME, 'query')
sleep(0.5)
input_place.send_keys(city)
sleep(0.5)
input_place.submit()
sleep(0.5)
btn_stay = browser.find_element(By.CSS_SELECTOR, 'button > img')
btn_stay.click()
sleep(2)
btn_next = browser.find_element(By.CSS_SELECTOR, 'footer > button')
btn_next.click()
sleep(2)
btn_next = browser.find_element(By.CSS_SELECTOR, 'footer > button')
btn_next.click()
sleep(5)

#select the list of items
page_content = browser.page_source
site = BeautifulSoup(page_content, 'html.parser')
rooms_data = []
rooms = site.findAll('div', attrs={'id': re.compile('^listing-.*')})

#collect the info
for room in rooms:
    room_name = room.find('span', attrs={'id': re.compile('^title_.*')}).text.strip()
    room_desc = room.select('ol > li')
    room_loc = room_desc[1].text.replace(' · ', '')
    room_desc = room_desc[0].text
    room_price = room.findAll('span')[-1].text
    room_link = room.find('a', attrs={'href': re.compile('^/rooms/.*')})
    room_link = 'http://airbnb.com' + room_link['href']
    rooms_data.append([room_name, room_loc, room_desc, room_price, room_link])

#export the info into a file
data = pd.DataFrame(rooms_data, columns=['Name', 'Location', 'Description', 'Price', 'Link'])
data.to_csv('rooms.csv', index=False)

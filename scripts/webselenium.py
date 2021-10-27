from selenium import webdriver
from time import sleep

browser = webdriver.Chrome()

browser.get('https://www.walissonsilva.com/blog')

sleep(3)

element = browser.find_element_by_tag_name('input')

element.send_keys('data')

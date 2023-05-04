from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging, os, time
import urllib.request
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
logging.disable()



dir_path = 'images'

#wordSearch = input('What you want to search:') 
Word_Search = 'cat'
Number_of_pictures = 10


os.makedirs(dir_path, exist_ok=True)
browser = webdriver.Firefox()
browser.get('https://imgur.com/')
browser.maximize_window()
wait = WebDriverWait(browser, 20)


try:
    CookiesDisagree = browser.find_element(By.CLASS_NAME, 'css-47sehv')
    CookiesDisagree.click()
except:
    logging.debug('No cookies')

Search = browser.find_element(By.CLASS_NAME, 'Searchbar-textInput')
Search.send_keys('', Word_Search)
Search.send_keys(Keys.ENTER)

myElem = WebDriverWait(browser, 3).until(EC.presence_of_all_elements_located((By.ID, 'imagelist')))
del myElem

web = browser.find_element(By.TAG_NAME, 'html')


for x in range(Number_of_pictures//60 + 1):
    web.send_keys(Keys.DOWN)
    time.sleep(2)



Image = browser.find_elements(By.TAG_NAME, 'img')




if Image == []:
    logging.debug('Image not found')
else:
    for x in range(Number_of_pictures):
        if len(Image) > x:

            imageUrl = Image[x].get_attribute('src')
            try:
                urllib.request.urlretrieve(imageUrl, dir_path + '/' + Word_Search + '%s.jpg' % x)
            except:
                logging.debug('Was not able to download %s picture' % x)




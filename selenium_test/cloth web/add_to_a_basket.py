from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# start a Firefox browser session
driver = webdriver.Firefox()

# navigate to http://localhost:5000
driver.get("http://localhost:5000")

# find and click the element by XPATH
element = driver.find_element(By.XPATH, '/html/body/div[2]/div/ul/li[2]/a')
element.click()




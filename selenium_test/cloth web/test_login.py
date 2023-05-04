from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# start a Firefox browser session
driver = webdriver.Firefox()

# navigate to http://localhost:5000
driver.get("http://localhost:5000")

# find and click the element by XPATH
element = driver.find_element(By.XPATH, '/html/body/div[2]/div/ul/div/div/a[1]/i')
element.click()

# wait for the subpage to load
myElem = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="login"]')))

# find the login and password input fields, and enter text into them
login_field = driver.find_element(By.XPATH, '//*[@id="login"]')
login_field.send_keys("test")

password_field = driver.find_element(By.XPATH, '//*[@id="password"]')
password_field.send_keys("123")

# find and click the login button
login_button = driver.find_element(By.XPATH, '/html/body/div[3]/form/p[3]/input')
login_button.click()



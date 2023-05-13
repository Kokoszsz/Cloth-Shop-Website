from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Firefox()

driver.get("http://localhost:5000")

username = 'test'
password = '123'

element = driver.find_element(By.XPATH, '/html/body/div[2]/div/ul/div/div/a[1]/i')
element.click()

myElem = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="login"]')))

login_field = driver.find_element(By.XPATH, '//*[@id="login"]')
login_field.send_keys(username)

password_field = driver.find_element(By.XPATH, '//*[@id="password"]')
password_field.send_keys(password)

login_button = driver.find_element(By.XPATH, '/html/body/div[3]/form/p[3]/input[2]')
login_button.click()

try:
    welcome_text = driver.find_element(By.XPATH, '/html/body/div[2]/div/ul/div/li')
    print('User logged in')
    if username in welcome_text.text:
        print('Correct user is displayed')
    else:
        print('Wrong user is displayed')

    logout_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/ul/div/div/a[3]')
    logout_button.click()

    try:
        welcome_text = driver.find_element(By.XPATH, '/html/body/div[2]/div/ul/div/li')
        print('User is still logged in')
    except:
        print('User was successfully been logged out')

except:
    print('User was not able to log in')





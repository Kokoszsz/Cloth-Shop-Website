from selenium import webdriver
from selenium.webdriver.common.by import By



driver = webdriver.Chrome()

driver.get('http://localhost:5000')

cloth_subpage = driver.find_element(By.XPATH, '/html/body/div[2]/div/ul/li[2]/a')
cloth_subpage.click()

filters = [
    {'category': 't-shirt', 'gender': 'male', 'price_min': '30', 'price_max': '70'},
    {'category': 'jeans', 'gender': 'female', 'price_min': '60', 'price_max': '100'},
    {'category': 'shirt', 'gender': 'male', 'price_min': '5', 'price_max': '30'},
]

for filter_data in filters:
    category = driver.find_element(By.NAME, filter_data['category'])
    category.click()

    gender = driver.find_element(By.NAME, filter_data['gender'])
    gender.click()
    
    price_min_input = driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/form/div[2]/input[1]')
    price_min_input.clear()
    price_min_input.send_keys(filter_data['price_min'])
    
    price_max_input = driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/form/div[2]/input[2]')
    price_max_input.clear()
    price_max_input.send_keys(filter_data['price_max'])

    filter_button = driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/form/input')
    filter_button.click()

    print(filter_data['category'])
    print(filter_data['gender'])
    print(filter_data['price_min'])
    print(filter_data['price_max'])
    
    input('Press Enter to continue after verifying the displayed products...')

    category.click()
    gender.click()








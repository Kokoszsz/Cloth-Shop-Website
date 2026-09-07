from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Firefox()

driver.get("http://localhost:5000")
driver.maximize_window()

cloth_subpage = driver.find_element(By.XPATH, '/html/body/div[2]/div/ul/li[2]/a')
cloth_subpage.click()

for x in range(1,10):
    try:
        cloth_name = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div[{0}]/div/div/a/h2'.format(x))
        cloth_name = cloth_name.text
        add_product = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div[{0}]/div/a'.format(x))
        add_product.click()


        ok = driver.find_element(By.XPATH, '/html/body/div[5]/div/a')
        ok.click()

        basket = driver.find_element(By.XPATH, '/html/body/div[2]/div/ul/div/div/a[2]')
        basket.click()
        if x == 1:
            basket = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[4]/div/div/div[1]/h3')))
            basket_name = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[1]/h3')
            basket_name = basket_name.text
        else:
            basket = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[4]/div/div[{0}]/div[1]/h3'.format(x))))
            basket_name = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[{0}]/div[1]/h3'.format(x))
            basket_name = basket_name.text


        print(basket_name)
        cloth_subpage = driver.find_element(By.XPATH, '/html/body/div[2]/ul/li[2]/a')
        cloth_subpage.click()

        if cloth_name == basket_name:
            print('%s. OK' % x)
        else:
            print('%s. Names do not mach ' % x)

    except:
        print('%s. ERROR, element not found' % x)





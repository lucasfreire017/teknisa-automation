from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome(executable_path=r"../webdriver/chromedriver.exe") # version 91
driver.get("https://retail.teknisa.com/login/#/login#authentication")
sleep(5)
driver.find_element_by_name("USER").send_keys("estoque.cj@pobrejuan.com.br" + Keys.TAB)
driver.find_element_by_xpath('//*[@id="PASSWORD"]').send_keys("20200201" + Keys.TAB)
driver.find_element_by_xpath('//*[@id="SUBMIT"]').click()
sleep(8)


# Alert about another user
def usuario():
    try:
        driver.find_element_by_xpath('/html/body/span/section/section/div[2]/aside[1]/aside/section/aside')
    except:
        return False

    finally:
        return True


# This function will wait a set time until the element is visible
def wait(*class_name):

    element = WebDriverWait(driver, 120).until(presence_of_element_located((By.CLASS_NAME, class_name)))
    sleep(5)
    #show if the element was previewed
    if element.is_displayed() == False:
        print(f'Elemento visivel: {element.is_displayed()}')

# function responsible to write the start and final date of notes that will be searched in this form:
# (01/07/2021 - 31/07/2021) -> (0107202131072021)
def showdate():
    from datetime import date
    from calendar import monthrange

    year = date.today().year
    month = date.today().month
    lastDay = monthrange(year, month)[1]

    if month < 10:
        return f'010{month}{year}{lastDay}0{month}{year}'
    else:
        return f'01{month}{year}{lastDay}{month}{year}'


if usuario() == True:
    driver.find_element_by_xpath('/html/body/span/section/section/div[2]/aside[1]/aside/section/footer/button[1]').click()


wait('bars')
driver.find_element_by_xpath('//*[@id="header"]/div/div[2]/div[1]/a/div').click()
sleep(3)
driver.find_element_by_xpath('/html/body/span/section/section/div[2]/section[1]/div/aside/div[1]/section/input').send_keys('Importação/Consulta de Notas Fiscais (Arquivo XML)')
driver.find_element_by_xpath('/html/body/span/section/section/div[2]/section[1]/div/aside/div[2]/nav/ul/li/span/span[2]').click()


wait('popup-title')
driver.find_element_by_class_name('current').click()
driver.find_element_by_class_name('option').click()
sleep(1)
driver.find_element_by_xpath('//*[@id="popup"]/span/section/section/section/div/form/section[1]/div/div[3]/div[1]/div/div[2]/span').click()
driver.find_element_by_xpath('//*[@id="popup"]/span/section/section/section/div/form/section[1]/div/div[3]/div[1]/div/div[2]/ul/li[1]').click()
sleep(1)
# write the start and final dates of the 'DANFES' that will be filtered
driver.find_element_by_xpath('//*[@id="DTEMISSAO_START"]').send_keys(Keys.HOME, showdate())
sleep(2)
driver.find_element_by_xpath('//*[@id="footer"]/div[3]/ul/li/a/span').click()

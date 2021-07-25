from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait


# This function will wait a set time until the element is visible
def wait(class_name, text='', time=120):
    element = WebDriverWait(driver, time).until(presence_of_element_located((By.CLASS_NAME, class_name)))
    sleep(5)
    # show if the element was previewed
    if element.is_displayed() == False:
        print(f'Elemento \033[1m{text}\033[m não visualizado')
        return False
    else:
        print(f'Elemento \033[1m{text}\033[m visualizado')
        return True


def waitx(class_name, text='', time=120):
    element = WebDriverWait(driver, time).until(presence_of_element_located((By.XPATH, class_name)))
    sleep(5)
    # show if the element was previewed
    if element.is_displayed() == False:
        print(f'Elemento {text} não visualizado')
        return False
    else:
        print(f'Elemento {text} visualizado')
        return True


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


# function to getting the number of invoice that'll be searched
def initialNotes():
    file = open('../notas/Initial.txt', 'r', encoding='UTF-8')
    num = file.readline()
    file.close()

    return str(num)


# move the number of invoices not founds of main txt to error txt
def moveNum(num):
    fileInitial = open('../notas/Initial.txt', 'r+', encoding='UTF-8')
    fileError = open('../notas/Error.txt', 'a+', encoding='UTF-8')

    lines = fileInitial.readlines()

    fileInitial.seek(0)

    for line in lines:
        if line != num:
            fileInitial.write(line)
        else:
            fileError.write(num)
        fileInitial.truncate()

    fileInitial.close()
    fileError.close()


# <--- Main code --->

# Login
driver = webdriver.Chrome(executable_path=r"../webdriver/chromedriver.exe")  # version 91
driver.get("https://retail.teknisa.com/login/#/login#authentication")
sleep(5)
driver.find_element_by_name("USER").send_keys("estoque.cj@pobrejuan.com.br" + Keys.TAB)
driver.find_element_by_xpath('//*[@id="PASSWORD"]').send_keys("20200201" + Keys.TAB)
sleep(3)
driver.find_element_by_xpath('//*[@id="SUBMIT"]').click()
sleep(8)

if wait('zh-container-text-alert', 'alerta'):
    driver.find_element_by_xpath(
        '/html/body/span/section/section/div[2]/aside[1]/aside/section/footer/button[1]').click()

wait('bars', 'menu')
sleep(5)
driver.find_element_by_xpath('//*[@id="header"]/div/div[2]/div[1]/a/div').click()  # click to open container
sleep(5)
driver.find_element_by_xpath(
    '/html/body/span/section/section/div[2]/section[1]/div/aside/div[1]/section/input').send_keys(
    'Importação/Consulta de Notas Fiscais (Arquivo XML)')  # first option searched
driver.find_element_by_xpath(
    '/html/body/span/section/section/div[2]/section[1]/div/aside/div[2]/nav/ul/li/span/span[2]').click()

while True:
    try:
        wait('container', 'filtros', 15)
    except:
        driver.refresh()
    else:
        break

wait('current', 'Opção Unidade')
sleep(5)
driver.find_element_by_class_name('current').click()
wait('option', 'Inscrição Estadual Destino')
sleep(5)
driver.find_element_by_class_name('option').click()
sleep(3)
driver.find_element_by_xpath(
    '//*[@id="popup"]/span/section/section/section/div/form/section[1]/div/div[3]/div[1]/div/div[2]/span').click()
sleep(3)
driver.find_element_by_xpath(
    '//*[@id="popup"]/span/section/section/section/div/form/section[1]/div/div[3]/div[1]/div/div[2]/ul/li[1]').click()
sleep(2)
# write the start and final dates of the 'DANFES' that will be filtered
driver.find_element_by_xpath('//*[@id="DTEMISSAO_START"]').send_keys(Keys.HOME, showdate())
sleep(2)
driver.find_element_by_xpath('//*[@id="footer"]/div[3]/ul/li/a/span').click()  # Click when the filter is completed

wait('control-handle', 'botão de ações')
driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL, 'f')
sleep(2)
driver.find_element_by_xpath(
    '/html/body/span/section/section/div[2]/section[2]/div/section/section/div/section/div/div[2]/div/div[1]/ul/li['
    '3]/div/div/div/div[3]/input').send_keys(
    initialNotes())  # search an invoice

while True:
    try:
        waitx('//*[@id="grid-4037041933179304567641"]/div[2]/div/div/div/ng-include/p',
              '\033[1;31m"Notas não encontradas"\033[m', time=10)
    except:
        break
    else:
        moveNum(initialNotes())
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL, 'f')
        sleep(1)
        driver.find_element_by_xpath(
            '/html/body/span/section/section/div[2]/section[2]/div/section/section/div/section/div/div[2]/div/div['
            '1]/ul/li[ '
            '3]/div/div/div/div[3]/input').send_keys(initialNotes())

driver.find_element_by_xpath('//*[@id="grid-4037041933179304567641"]/div[2]/div/div[1]').click()

wait('zh-field-group', 'Informações da Nota')
x = driver.find_element_by_id('span-field-NRACESSONFE').text
print(type('key'))
key = x.strip('Chave de Acesso').split()[0]
print(f'A chave de Acesso é: {key}')

# Lançamento de entrada

# Open a new tab
driver.execute_script("window.open('https://retail.teknisa.com/df/#/df_entrada#dfe11000_lancamento_entrada', '_blank')")

# Change tab
driver.switch_to.window(1)
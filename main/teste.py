from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait


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


driver = webdriver.Chrome(executable_path=r"../webdriver/chromedriver.exe")  # version 91
driver.get('https://www.google.com/search?q=gato&oq=gato&aqs=chrome..69i57.1487j0j7&sourceid=chrome&ie=UTF-8')
sleep(3)
while True:
    driver.refresh()

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


def main():
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1200")
    DRIVER_PATH = '/media/corentin/Data/Cours/Perso/python/virtual-env/bin/chromedriver_linux64/chromedriver'

    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get("https://www.nba.com/stats/search/team-game/?CF=PTS*gt*0&Season=2019-20&SeasonType=Regular%20Season")

   

    ## si il y a une popup de cookies
    try:
        buttonCookie = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
        )
        buttonCookie.click()
        driver.implicitly_wait(5)
    except: 
        print("error: no cookie popup")

    # Si il y a un bouton permettant de charger plus de résultats, on charge jusqu'au bout
    try:
        buttonLoadMore = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "addrows__button"))
        )
        while buttonLoadMore != None :
            buttonLoadMore.click()
            buttonLoadMore = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "addrows__button"))
            )
            driver.implicitly_wait(0.2)
    except: 
        print("error : no button loadMore")


    # On récupère la page avec beautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #On crée le fichier csv
    createCsvFile(soup)

    driver.quit()


# Methode pemettant de lire la page web et de créer le fichier csv associé
def createCsvFile(soup):

    f = open("games.csv", 'a')
    thead = soup.find('thead')
    categoriesObject = thead.find_all('th')
    categories = []

    for category in categoriesObject:
        #print(category.text)
        f.write(category.text)
        f.write(';')
        categories.append(category.text)
    f.write('\n')


    rows = soup.find(class_="nba-stat-table__overflow").find_all('tr')
    for row in rows:
        #print(" - ")
        stats = row.find_all('td')
        i = 0
        for stat in stats:
            value = ""
            if(stat.a != None):
                value = (stat.a.text)
            else:
                value = (stat.text)
            # print(categories[i], ":",value )
            i=i+1
            f.write(value)
            f.write(';')
        f.write('\n')



    f.close()




# Entry Point for the application
if __name__ == '__main__':
    main()

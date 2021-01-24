# El script trabaja con ChromeDriver v88 para el navegador Google Chrome v88.
# Ejecutar comando 'pip install selenium' (en caso de no tenerlo instalado)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import time

# Indicar la ruta del chromedriver.exe v88 instalado.
PATH = "C:\\Program Files (x86)\\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# Ingreso a la URL que contiene el catálogo completo de Amazon Prime Video.
driver.get("https://www.amazon.com/gp/video/search/ref=atv_sr_breadcrumb_p_n_ways_to_watch?phrase=Romance&queryToken=eyJ0eXBlIjoiZmlsdGVyIiwibmF2Ijp0cnVlLCJzZWMiOiJjZW50ZXIiLCJzdHlwZSI6InNlYXJjaCIsInFyeSI6ImJibj0yODU4Nzc4MDExJnBfbl90aGVtZV9icm93c2UtYmluPSZzZWFyY2gtYWxpYXM9aW5zdGFudC12aWRlbyIsInR4dCI6IiIsImZpbHRlciI6e30sIm9mZnNldCI6MCwibnBzaSI6MCwib3JlcSI6ImY5NzQzYjkyLWQ4NjUtNGViZS04NjQzLWVmMTE5MzZhYTU5ZjoxNjExMjg2MzQyMDAwIiwic3RLZXkiOiJ7XCJzYnNpblwiOjAsXCJjdXJzaXplXCI6MCxcInByZXNpemVcIjowfSIsIm9yZXFrIjoiTGk2K28vZ3NoMGhHQ2NUZ2FUZ0tMem1iQXp0em5nb3NvZUkwNnphaGZkST0iLCJvcmVxa3YiOjF9&ie=UTF8&pageId=default&queryPageType=browse")

# Sentencia while para ir hasta el final de la página, garantizando que se cargan todos los contenidos del catálogo.
# def scrolldown():
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     while True:
#         driver.execute_script("scrollTo(0, document.body.scrollHeight);")
#         time.sleep(5)
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height

# Funcion utilizada para determinar si un contenido cuenta con episodios (por lo tanto corresponde a una serie)
def has_episodes(url):

    clickable_elements = url.find_element_by_xpath('//*[@id="a-page"]/div[4]/div[3]/div/div/div[2]/div')
    clickables = clickable_elements.find_elements_by_class_name('_2U-UfT')
    return clickables[1].text == "Episodios"

# Creo una lista para guardar los titulos dado que Prime Video a veces repite titulos porque los separa por temporadas, de esta forma se evitan duplicaciones.
content_titles = []

# Obtengo el listado con todos los contenidos de la página y comienzo a iterar uno por uno.
def main():
    # scrolldown()
    contents = driver.find_elements_by_class_name('av-hover-wrapper')
    for content in contents:
        content_name = content.find_element_by_class_name('av-beard-title-link')
        title = content_name.text
        # Si el título del contenido ya aparece en el listado significa que ya fue analizado.
        # if not content_titles.__contains__(title):
        content_link = content_name.get_attribute('href')
        
        # Abro una nueva pestaña para ver uno a uno los contenidos.
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(content_link)

        # Determino si un contenido cuenta con episodios (por lo tanto corresponde a una serie)
        clickable_elements = driver.find_element_by_xpath('//*[@id="a-page"]/div[4]/div[3]/div/div/div[2]/div')
        clickables = clickable_elements.find_elements_by_class_name('_2U-UfT')
        if clickables[0].text == "Episodes":
            # aca iria el scraping por serie 
            title += " ES UNA SERIE"
        else:
            # aca iria el scraping por pelicula 
            title += " ES UNA PELICULA"
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        content_titles.append(title)

    print(content_titles)

if __name__ == "__main__":
    main()    

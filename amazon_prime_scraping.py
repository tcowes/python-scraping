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

# Funcion para ubicar el año de estreno del titulo
# def get_release_year():

def tv_show_scraping():
    # TODO: CORREGIR, NO TOMA BIEN LOS DIRECTORES 
    # Container de la sección de elementos cliqueables (para buscar el detalle con los directores)
    clickable_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="a-page"]/div[4]/div[3]/div/div/div[2]/div'))
    )
    clickables = clickable_elements.find_elements_by_class_name('_2U-UfT')
    for clickable in clickables:
        if clickable.text == "Details":
            clickable.click()
            break
    xpath_for_first_detail = driver.find_element_by_xpath('//*[@id="btf-product-details"]/div/dl[1]/dt/span')
    if xpath_for_first_detail.text == "Directors":
        directors = driver.find_element_by_xpath('//*[@id="btf-product-details"]/div/dl[1]/dd').text
    else:
        directors = "directores no especificados"

    # Creacion del diccionario que va a contener toda la informacion relevante de cada titulo de tipo serie
    data = {
        "año": driver.find_element_by_css_selector('span[data-automation-id="release-year-badge"]').text,
        "directores": directors,
        "actores": driver.find_element_by_xpath('//*[@id="meta-info"]/div/dl[1]/dd').text,
        "link": driver.current_url,
        "descripción": driver.find_element_by_xpath('/html/head/meta[4]').get_attribute('content'),
        "generos": driver.find_element_by_xpath('//*[@id="meta-info"]/div/dl[2]/dd').text,
        "rating": driver.find_element_by_xpath('//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[1]/div/div[2]/div/span/span').text 
        + " stars (" + driver.find_element_by_xpath('//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[2]/span').text + ")",
        "tipo": "Serie"
    }
    return data

def movie_scraping():
    # Creacion del diccionario que va a contener toda la informacion relevante de cada titulo de tipo pelicula
    data = {
        "año": driver.find_element_by_css_selector('span[data-automation-id="release-year-badge"]').text,
        "directores": driver.find_element_by_xpath('//*[@id="meta-info"]/div/dl[1]/dd').text,
        "actores": driver.find_element_by_xpath('//*[@id="meta-info"]/div/dl[2]/dd').text,
        "link": driver.current_url,
        "descripción": driver.find_element_by_xpath('/html/head/meta[4]').get_attribute('content'),
        "generos": driver.find_element_by_xpath('//*[@id="meta-info"]/div/dl[3]/dd').text,
        "rating": driver.find_element_by_xpath('//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[1]/div/div[2]/div/span/span').text 
        + " stars (" + driver.find_element_by_xpath('//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[2]/span').text + ")",
        "tipo": "Pelicula"
    }
    return data

# Imprimo de forma indentada cada key-value del diccionario pasado por parametros
def print_dictionary(dict):
    for key, value in dict.items():
        print(key, ':', value)

# Creo una lista para guardar los titulos dado que Prime Video a veces repite titulos porque los separa por temporadas, de esta forma se evitan duplicaciones.
content_titles = []

# Creo una lista para almacenar la data de cada titulo
content_data = []

# Obtengo el listado con todos los contenidos de la página y comienzo a iterar uno por uno.
def main():
    # scrolldown()
    content_hovers = driver.find_elements_by_class_name('av-hover-wrapper')
    for content in content_hovers:
        content_name = content.find_element_by_class_name('av-beard-title-link')
        title = content_name.text
        # Si el título del contenido ya aparece en el listado significa que ya fue analizado.
        # if not content_titles.__contains__(title):
        content_link = content_name.get_attribute('href')
        
        # Abro una nueva pestaña para ver uno a uno los contenidos.
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(content_link)

        # Determino si un contenido cuenta con episodios (por lo tanto corresponde a una serie).
        clickable_elements = driver.find_element_by_xpath('//*[@id="a-page"]/div[4]/div[3]/div/div/div[2]/div')
        clickables = clickable_elements.find_elements_by_class_name('_2U-UfT')
        if clickables[0].text == "Episodes":
            content_data.append(tv_show_scraping())
        else:
            content_data.append(movie_scraping())
        
        # Cierro la ventana y vuelvo a la pagina principal.
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        content_titles.append(title)

    # Inicializo un indice para iterar y agregarle los titulos a cada contenido con sus datos.
    i = 0
    for data in content_data:
        print("titulo : " + content_titles[i])
        print_dictionary(data)
        print("\n")
        i += 1

if __name__ == "__main__":
    main()    
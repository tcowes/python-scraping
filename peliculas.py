from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = 'C:\\Program Files (x86)\\chromedriver.exe'
driver = webdriver.Chrome(PATH)

driver.get("https://www.amazon.com/gp/video/detail/B08L48LTPY/ref=atv_br_def_r_br_c_unkc_1_5")

try:
    # Creacion del diccionario que va a contener toda la informacion relevante de cada titulo
    datos_pelicula = {
        "titulo": driver.find_element_by_xpath('//*[@id="a-page"]/div[4]/div[2]/div/div/div[2]/div[2]/div/h1').text,
        "año": driver.find_element_by_xpath('//*[@id="a-page"]/div[4]/div[2]/div/div/div[2]/div[2]/div/div[1]/span[3]/span').text,
        "directores": driver.find_element_by_xpath('//*[@id="meta-info"]/div/dl[1]/dd').text,
        "actores": driver.find_element_by_xpath('//*[@id="meta-info"]/div/dl[2]/dd').text,
        "link": driver.current_url,
        "descripción": driver.find_element_by_xpath('//*[@id="a-page"]/div[4]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div/div/div').text,
        "generos": driver.find_element_by_xpath('//*[@id="meta-info"]/div/dl[3]/dd').text,
        "rating": driver.find_element_by_xpath('//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[1]/div/div[2]/div/span/span').text 
        + " stars (" + driver.find_element_by_xpath('//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[2]/span').text + ")",
        "tipo": "Pelicula"
    }

    # Imprimo cada valor del diccionario
    for key, value in datos_pelicula.items():
        print(key, ':', value)
finally:
    driver.quit()

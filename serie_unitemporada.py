from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.amazon.com/gp/video/detail/B084L2DNXT/ref=atv_br_def_r_br_c_unkc_1_9")

# Este script se utiliza con las series que tienen mas de una temporada

try:
    # Container de la sección de información
    tv_show_info = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "_15BvJ7"))
    )

    # Container de la sección de episodios
    seccion_capitulos = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "_3KHiTg"))
    )

    # Esta parte del diccionario esta escrita manualmente por cada TV show para agarrar
    # lo mas relevante de la sección info de la pagina de la serie en netflix.
    #
    # Luego, automaticamente se agregan al diccionario las sinopsis 
    # de cada uno de los capitulos, separado por temporada.
    datos_serie = {
        "Título": tv_show_info.find_element_by_class_name("_1GTSsh _2Q73m9").text,
        # "Año": tv_show_info.find_element_by_css_selector("span[data-automation-id='release-year-badge']").text,
        # "Directores": ,
        # Actores": tv_show_info.find_elements_by_class_name("_1NNx6V").text,
        "Link": "link juas",
        "Descripción": tv_show_info.find_element_by_class_name("_1W5VSv").text,
        # "Géneros": tv_show_info.find_element_by_class_name("_1NNx6V").text, TIENE EL MISMO CLASSNAME
        # "Rating": tv_show_info.find_element_by_css_selector("span[data-automation-id='imdb-rating-badge']").text,
        "Tipo": "Serie de TV"
    }

    # Agrego llaves y valores de cada temporada y episodios al dict datos_serie
    episodios = driver.find_elements_by_class_name("_1FuiMq js-node-episode-container f11d1lkh")

    for episodio in episodios:
        episodio_titulo = episodio.find_element_by_class_name("_1TQ2Rs").text
        episodio_sinopsis = episodio.find_element_by_class_name("_3qsVvm _19hYO2").text

        if episodio_titulo[1] == ".":
            datos_serie[f"T{i+1}E{episodios.index(episodio)+1}"] = episodio_titulo[3:]
        else:
            datos_serie[f"T{i+1}E{episodios.index(episodio)+1}"] = episodio_titulo[4:]

        datos_serie[f"T{i+1}E{episodios.index(episodio)+1} Sinopsis"] = episodio_sinopsis
    
    # Imprimo cada valor del diccionario datos_serie
    for key, value in datos_serie.items():
        print(key, ':', value)
finally:
    driver.quit()
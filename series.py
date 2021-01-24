from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = 'C:\\Program Files (x86)\\chromedriver.exe'
driver = webdriver.Chrome(PATH)

driver.get("https://www.amazon.com/gp/video/detail/B084L2DNXT/ref=atv_br_def_r_br_c_unkc_1_9")

try:
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
    if xpath_for_first_detail.text == "Dirección":
        directors = driver.find_element_by_xpath('//*[@id="btf-product-details"]/div/dl[1]/dd').text
    else:
        directors = "directores no especificados"

    # Creacion del diccionario que va a contener toda la informacion relevante de cada titulo
    datos_serie = {
        "titulo": driver.find_element_by_xpath('//*[@id="a-page"]/div[4]/div[2]/div/div/div[2]/div[2]/div/h1').text,
        "año": driver.find_element_by_xpath('//*[@id="a-page"]/div[4]/div[2]/div/div/div[2]/div[2]/div/div[1]/span[2]/span').text,
        "directores": directors,
        "actores": driver.find_element_by_xpath('//*[@id="meta-info"]/div/dl[1]/dd').text,
        "link": driver.current_url,
        "descripción": driver.find_element_by_xpath('//*[@id="a-page"]/div[4]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div/div/div').text,
        "generos": driver.find_element_by_xpath('//*[@id="meta-info"]/div/dl[2]/dd').text,
        "rating": driver.find_element_by_xpath('//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[1]/div/div[2]/div/span/span').text 
        + " stars (" + driver.find_element_by_xpath('//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[2]/span').text + ")",
        "tipo": "Serie"
    }

    # Imprimo cada valor del diccionario
    for key, value in datos_serie.items():
        print(key, ':', value)
finally:
    driver.quit()

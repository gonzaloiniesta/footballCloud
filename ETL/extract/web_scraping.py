from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Configuración del navegador
options = Options()
# options.add_argument('--headless')  # Ejecuta sin interfaz gráfica (opcional)
driver_service = Service('/usr/bin/chromedriver')
driver = webdriver.Chrome(service=driver_service, options=options)


def get_player_clasic_data():

    driver.get("https://www.laliga.com/estadisticas-avanzadas")

    all_data = []  # Lista para almacenar todos los datos

    time.sleep(5)
        
    accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
    )
        
    accept_button.click()

    while True:

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[6]/div[3]'))
        )

        table = driver.find_element(By.XPATH, '//*[@id="__next"]/div[6]/div[3]')
        rows = table.find_elements(By.TAG_NAME, "tr")

        if not all_data:
            headers = rows[0].find_elements(By.TAG_NAME, "th")
            column_names = [header.text for header in headers]

        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, "td")
            cols = [col.text for col in cols]
            if cols:
                all_data.append(cols)

        print("Realizando dos desplazamientos hacia abajo...")
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)


        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[4]/div/div/div/div[5]'))
            )
            print("Pulsando el botón para ir a la siguiente página...")
            next_button.click()
            time.sleep(10)
        except Exception as e:
            print("No hay más páginas disponibles o botón no encontrado.")
            break

    df = pd.DataFrame(all_data, columns=column_names)
    print(df)
    df.to_csv("estadisticas_jugadores_laliga.csv", index=False)

    driver.quit()

def get_player_eficiencia_data():

    driver.get("https://www.laliga.com/estadisticas-avanzadas")

    all_data = []  # Lista para almacenar todos los datos

    time.sleep(5)
        
    accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
    ).click()


    time.sleep(2) 

    desplegable = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[1]/div/div[2]/div[2]/div/div/div[1]'))
    ).click()
    time.sleep(5)

    eficiencia = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[1]/div/div[2]/div[2]/div/ul/li[2]'))
    ).click()

    time.sleep(8)

    while True:

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[6]/div[3]'))
        )

        table = driver.find_element(By.XPATH, '//*[@id="__next"]/div[6]/div[3]')
        rows = table.find_elements(By.TAG_NAME, "tr")

        if not all_data:
            headers = rows[0].find_elements(By.TAG_NAME, "th")
            column_names = [header.text for header in headers]

        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, "td")
            cols = [col.text for col in cols]
            if cols:
                all_data.append(cols)

        print("Realizando dos desplazamientos hacia abajo...")
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)


        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[4]/div/div/div/div[5]'))
            )
            print("Pulsando el botón para ir a la siguiente página...")
            next_button.click()
            time.sleep(10)
        except Exception as e:
            print("No hay más páginas disponibles o botón no encontrado.")
            break

    df = pd.DataFrame(all_data, columns=column_names)
    print(df)
    df.to_csv("estadisticas_jugadores_eficiencia_laliga.csv", index=False)

    driver.quit()

def get_player_disciplina_data():

    driver.get("https://www.laliga.com/estadisticas-avanzadas")

    all_data = []  # Lista para almacenar todos los datos

    time.sleep(5)
        
    accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
    ).click()

    time.sleep(2) 

    desplegable = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[1]/div/div[2]/div[2]/div/div/div[1]'))
    ).click()

    time.sleep(5)

    disciplina = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[1]/div/div[2]/div[2]/div/ul/li[3]'))
    ).click()

    time.sleep(8)

    while True:

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[6]/div[3]'))
        )

        table = driver.find_element(By.XPATH, '//*[@id="__next"]/div[6]/div[3]')
        rows = table.find_elements(By.TAG_NAME, "tr")

        if not all_data:
            headers = rows[0].find_elements(By.TAG_NAME, "th")
            column_names = [header.text for header in headers]

        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, "td")
            cols = [col.text for col in cols]
            if cols:
                all_data.append(cols)

        print("Realizando dos desplazamientos hacia abajo...")
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)


        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[4]/div/div/div/div[5]'))
            )
            print("Pulsando el botón para ir a la siguiente página...")
            next_button.click()
            time.sleep(10)
        except Exception as e:
            print("No hay más páginas disponibles o botón no encontrado.")
            break

    df = pd.DataFrame(all_data, columns=column_names)
    print(df)
    df.to_csv("estadisticas_jugadores_disciplina_laliga.csv", index=False)

    driver.quit()

def get_player_ataques_data():

    driver.get("https://www.laliga.com/estadisticas-avanzadas")

    all_data = []  # Lista para almacenar todos los datos

    time.sleep(5)
        
    accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
    ).click()

    time.sleep(2) 

    desplegable = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[1]/div/div[2]/div[2]/div/div/div[1]'))
    ).click()

    time.sleep(5)

    ataques = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[1]/div/div[2]/div[2]/div/ul/li[4]'))
    ).click()

    time.sleep(8)

    while True:

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[6]/div[3]'))
        )

        table = driver.find_element(By.XPATH, '//*[@id="__next"]/div[6]/div[3]')
        rows = table.find_elements(By.TAG_NAME, "tr")

        if not all_data:
            headers = rows[0].find_elements(By.TAG_NAME, "th")
            column_names = [header.text for header in headers]

        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, "td")
            cols = [col.text for col in cols]
            if cols:
                all_data.append(cols)

        print("Realizando dos desplazamientos hacia abajo...")
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)


        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[4]/div/div/div/div[5]'))
            )
            print("Pulsando el botón para ir a la siguiente página...")
            next_button.click()
            time.sleep(10)
        except Exception as e:
            print("No hay más páginas disponibles o botón no encontrado.")
            break

    df = pd.DataFrame(all_data, columns=column_names)
    print(df)
    df.to_csv("estadisticas_jugadores_ataques_laliga.csv", index=False)

    driver.quit()

def get_player_defensiva_data():

    driver.get("https://www.laliga.com/estadisticas-avanzadas")

    all_data = []  # Lista para almacenar todos los datos

    time.sleep(5)
        
    accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
    ).click()

    time.sleep(2) 

    desplegable = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[1]/div/div[2]/div[2]/div/div/div[1]'))
    ).click()

    time.sleep(5)

    defensiva = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[1]/div/div[2]/div[2]/div/ul/li[5]'))
    ).click()

    time.sleep(8)

    while True:

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[6]/div[3]'))
        )

        table = driver.find_element(By.XPATH, '//*[@id="__next"]/div[6]/div[3]')
        rows = table.find_elements(By.TAG_NAME, "tr")

        if not all_data:
            headers = rows[0].find_elements(By.TAG_NAME, "th")
            column_names = [header.text for header in headers]

        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, "td")
            cols = [col.text for col in cols]
            if cols:
                all_data.append(cols)

        print("Realizando dos desplazamientos hacia abajo...")
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)


        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[4]/div/div/div/div[5]'))
            )
            print("Pulsando el botón para ir a la siguiente página...")
            next_button.click()
            time.sleep(10)
        except Exception as e:
            print("No hay más páginas disponibles o botón no encontrado.")
            break

    df = pd.DataFrame(all_data, columns=column_names)
    print(df)
    df.to_csv("estadisticas_jugadores_defensiva_laliga.csv", index=False)

    driver.quit()


def get_league_clasica_data():
    
    driver.get("https://www.laliga.com/estadisticas-avanzadas")
    all_data = []
    time.sleep(5)

    accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
    ).click()
    leage_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[2]/div/div/div[2]/p'))
    ).click()


    time.sleep(10)
        
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[6]/div[3]'))
    )

    table = driver.find_element(By.XPATH, '//*[@id="__next"]/div[6]/div[3]')
    rows = table.find_elements(By.TAG_NAME, "tr")

    if not all_data:
        headers = rows[0].find_elements(By.TAG_NAME, "th")
        column_names = [header.text for header in headers]

    for row in rows[1:]:
        cols = row.find_elements(By.TAG_NAME, "td")
        cols = [col.text for col in cols]
        if cols:
            all_data.append(cols)

    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(1)
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(1)

    df = pd.DataFrame(all_data, columns=column_names)
    print(df)
    df.to_csv("estadisticas_laliga.csv", index=False)

    driver.quit()

def get_league_eficiencia_data():
    
    driver.get("https://www.laliga.com/estadisticas-avanzadas")
    all_data = []
    time.sleep(5)

    accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
    ).click()
    leage_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[2]/div/div/div[2]/p'))
    ).click()

    time.sleep(2) 
    desplegable = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[1]/div/div[2]/div[2]/div/div/div[1]'))
    ).click()
    time.sleep(5)

    eficiencia = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[1]/div/div[2]/div[2]/div/ul/li[2]'))
    ).click()
    time.sleep(8)



    time.sleep(10)
        
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[6]/div[3]'))
    )

    table = driver.find_element(By.XPATH, '//*[@id="__next"]/div[6]/div[3]')
    rows = table.find_elements(By.TAG_NAME, "tr")

    if not all_data:
        headers = rows[0].find_elements(By.TAG_NAME, "th")
        column_names = [header.text for header in headers]

    for row in rows[1:]:
        cols = row.find_elements(By.TAG_NAME, "td")
        cols = [col.text for col in cols]
        if cols:
            all_data.append(cols)

    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(1)
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(1)

    df = pd.DataFrame(all_data, columns=column_names)
    print(df)
    df.to_csv("estadisticas_eficiencia_laliga.csv", index=False)

    driver.quit()


def get_league_ataque_data():
    pass

def get_league_defensiva_data():
    pass

def get_league_disciplina_data():
    pass


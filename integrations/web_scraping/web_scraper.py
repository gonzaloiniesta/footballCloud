from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from enum import Enum

class DataType(Enum):
    CLASICO = "Clásico"
    EFICIENCIA = "Eficiencia"
    DISCIPLINA = "Disciplina"
    ATAQUES = "Ataques"
    DEFENSIVA = "Defensiva"

class FootballScraper:
    def __init__(self, driver):
        """
        Constructor to initialize the scraper with the Selenium WebDriver.
        -param driver: Instance of the Selenium WebDriver.
        """
        self.driver = driver
        self.base_url = "https://www.laliga.com/estadisticas-avanzadas"
        self.option_xpath = {
            DataType.EFICIENCIA: '//*[@id="__next"]/div[6]/div[1]/div/div[2]/div[2]/div/ul/li[2]',
            DataType.DISCIPLINA: '//*[@id="__next"]/div[6]/div[1]/div/div[2]/div[2]/div/ul/li[3]',
            DataType.ATAQUES: '//*[@id="__next"]/div[6]/div[1]/div/div[2]/div[2]/div/ul/li[4]',
            DataType.DEFENSIVA: '//*[@id="__next"]/div[6]/div[1]/div/div[2]/div[2]/div/ul/li[5]'
        }

    def get_data(self, data_type: DataType, is_league: bool = False, isFirst: bool = False, output_file=None):
        """
        Generic method to extract LaLiga's information.
        -param data_type: Type of data (DataType Enum).
        -param output_file: Name of the output CSV file.
        -param is_league: Indicates whether the data is for the league (True) or players (False).
        """
        self.driver.get(self.base_url)
        all_data = []

        time.sleep(5)
        
        if isFirst:
            # Accept cookies
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
            ).click()

        # Switch to league view if required
        if is_league:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[2]/div/div/div[2]/p'))
            ).click()
            time.sleep(5)

        # If not "Clásico", select the type from the dropdown
        if data_type != DataType.CLASICO:
            dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[1]/div/div[2]/div[2]/div/div/div[1]'))
            ).click()
            time.sleep(2)

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.option_xpath[data_type]))
            ).click()
            time.sleep(5)

        while True:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[6]/div[3]'))
            )

            table = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[6]/div[3]')
            rows = table.find_elements(By.TAG_NAME, "tr")

            if not all_data:
                headers = rows[0].find_elements(By.TAG_NAME, "th")
                column_names = [header.text for header in headers]

            for row in rows[1:]:
                cols = row.find_elements(By.TAG_NAME, "td")
                cols = [col.text for col in cols]
                if cols:
                    all_data.append(cols)

            print("Performing two scrolls down...")
            self.driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)
            self.driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)

            try:
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[6]/div[4]/div/div/div/div[5]'))
                )
                print("Clicking the button to go to the next page...")
                next_button.click()
                time.sleep(5)
            except Exception:
                print("No more pages available or button not found.")
                break

        df = pd.DataFrame(all_data, columns=column_names)

        if output_file is not None:
            df.to_csv(output_file, index=False)

        return df

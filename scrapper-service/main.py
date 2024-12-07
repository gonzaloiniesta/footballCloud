from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from extract import LaLigaScraper, DataType


options = Options()
# options.add_argument('--headless')

driver_service = Service('/usr/bin/chromedriver')
driver = webdriver.Chrome(service=driver_service, options=options)

scraper = LaLigaScraper(driver)

# Player data extraction
# scraper.get_data(DataType.EFICIENCIA, output_file="player_efficiency_stats.csv", is_league=False, isFirst=True)
# scraper.get_data(DataType.DISCIPLINA, output_file="player_discipline_stats.csv", is_league=False, isFirst=False)
# scraper.get_data(DataType.ATAQUES, output_file="player_attack_stats.csv", is_league=False, isFirst=False)
# scraper.get_data(DataType.DEFENSIVA, output_file="player_defensive_stats.csv", is_league=False, isFirst=True)
# scraper.get_data(DataType.CLASICO, output_file="player_classic_stats.csv", is_league=False, isFirst=False)


# League data extraction
scraper.get_data(DataType.EFICIENCIA, output_file="league_efficiency_stats.csv", is_league=True, isFirst=True)
scraper.get_data(DataType.DISCIPLINA, output_file="league_discipline_stats.csv", is_league=True, isFirst=False)
scraper.get_data(DataType.ATAQUES, output_file="league_attack_stats.csv", is_league=True, isFirst=False)
scraper.get_data(DataType.DEFENSIVA, output_file="league_defensive_stats.csv", is_league=True, isFirst=False)
scraper.get_data(DataType.CLASICO, output_file="league_classic_stats.csv", is_league=True, isFirst=False)


driver.quit()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from integrations import FootballScraper, KafkaProducerFootballCloud, DataType
from pandas import DataFrame
import unicodedata

def setup_driver():
    options = Options()
    # options.add_argument('--headless')  # Descomentar para ejecutar sin interfaz gráfica
    driver_service = Service('/usr/bin/chromedriver')  # Ajusta la ruta si es necesario
    driver = webdriver.Chrome(service=driver_service, options=options)
    return driver

def remove_accents(text: str):
    """Remove accents from a given string."""
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(char for char in normalized if unicodedata.category(char) != 'Mn')

def publish_dataframe_to_kafka(producer, df: DataFrame, data_type, topic: str, isLeague: bool):
    """Publishes each row of the DataFrame as a JSON message to a specified Kafka topic."""
    
    for _, row in df.iterrows():
        msg = row.to_dict()

        if isLeague:
            key = {
                "team": remove_accents(str(msg["EQUIPO"])),
                "stats": remove_accents(data_type.value)
                }
        else:
            key = {
                "player": remove_accents(str(msg["NOMBRE"])),
                "stats": remove_accents(data_type.value)
                }

        producer.publish(topic=topic, key=key, message=msg)




def extract_and_publish(scraper, producer, data_types, is_league, prefix, topic):
    """Extracts data using the scraper and publishes it to a specified Kafka topic."""
    for index, data_type in enumerate(data_types):
        is_first = index == 0
        df = scraper.get_data(data_type, is_league=is_league, isFirst=is_first)
        publish_dataframe_to_kafka(producer=producer, df=df, data_type=data_type, topic=topic, isLeague=is_league)



if __name__ == "__main__":
    driver = setup_driver()
    scraper = FootballScraper(driver)

    KAFKA_URL = "localhost"
    KAFKA_PORT = 9092

    producer = KafkaProducerFootballCloud(KAFKA_URL, KAFKA_PORT)

    data_types = [
        # DataType.EFICIENCIA,
        # DataType.DISCIPLINA,
        DataType.ATAQUES,
        # DataType.DEFENSIVA,
        # DataType.CLASICO
    ]

    try:
       
        # extract_and_publish(scraper, producer, data_types, is_league=True, prefix="league", topic="league_stats")
        extract_and_publish(scraper, producer, data_types, is_league=False, prefix="player", topic="player_stats")

    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

    finally:
        driver.quit()
        print("WebDriver closed.")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from integrations import LaLigaScraper, KafkaProducerFootballCloud, DataType
from pandas import DataFrame

def setup_driver():
    options = Options()
    # options.add_argument('--headless')  # Descomentar para ejecutar sin interfaz gráfica
    driver_service = Service('/usr/bin/chromedriver')  # Ajusta la ruta si es necesario
    driver = webdriver.Chrome(service=driver_service, options=options)
    return driver

def remove_accents(text: str):
    """Remove accents from a given string."""
    return text.encode('ascii', 'ignore').decode('utf-8')

def publish_dataframe_to_kafka(producer, df: DataFrame, data_type, topic: str, isLeague: bool):
    """Publishes each row of the DataFrame as a JSON message to a specified Kafka topic."""
    try:
        for _, row in df.iterrows():
            msg = row.to_dict()
            key = {
                "team": remove_accents(str(msg["EQUIPO"])) if isLeague else remove_accents(msg["NOMBRE"]),
                "stats": data_type.value
            }
            producer.publish(topic=topic, key=key, message=msg)
    except Exception as e:
        print(f"❌ Error while publishing data: {e}")

def extract_and_publish(scraper, producer, data_types, is_league, prefix, topic):
    """Extracts data using the scraper and publishes it to a specified Kafka topic."""
    for index, data_type in enumerate(data_types):
        is_first = index == 0
        try:
            df = scraper.get_data(data_type, is_league=is_league, isFirst=is_first)
            publish_dataframe_to_kafka(producer=producer, df=df, data_type=data_type, topic=topic, isLeague=is_league)
        except Exception as e:
            print(f"❌ Error occurred while processing {data_type.value}: {e}")

if __name__ == "__main__":
    driver = setup_driver()
    scraper = LaLigaScraper(driver)

    KAFKA_URL = "localhost"
    KAFKA_PORT = 9092

    producer = KafkaProducerFootballCloud(KAFKA_URL, KAFKA_PORT)

    data_types = [
        DataType.EFICIENCIA,
        DataType.DISCIPLINA,
        DataType.ATAQUES,
        DataType.DEFENSIVA,
        DataType.CLASICO
    ]

    try:
       
        extract_and_publish(scraper, producer, data_types, is_league=True, prefix="league", topic="league_stats")
        # extract_and_publish(scraper, producer, data_types, is_league=False, prefix="player", topic="player_stats")

    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

    finally:
        driver.quit()
        print("WebDriver closed.")

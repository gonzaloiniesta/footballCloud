from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from technologics_classes.webScrapingClass import LaLigaScraper, DataType
from technologics_classes.kafkaProducerClass import KafkaProducerFootballCloud
from kafka.errors import KafkaError
import json

def setup_driver():
    options = Options()
    # options.add_argument('--headless')  # Descomentar para ejecutar sin interfaz gráfica
    driver_service = Service('/usr/bin/chromedriver')  # Ajusta la ruta si es necesario
    driver = webdriver.Chrome(service=driver_service, options=options)
    return driver

def publish_dataframe_to_kafka(producer: KafkaProducerFootballCloud, df, data_type, topic):
    """
    Publishes each row of the DataFrame as a JSON message to Kafka.

    :param producer: Instance of KafkaProducerFootballCloud.
    :param df: DataFrame with the data to send.
    :param data_type: DataType Enum to add metadata.
    """
    try:
        for _, row in df.iterrows():
            # Convert each row to a dictionary and then to a JSON string
            message = {
                "data_type": data_type.value,
                "data": row.to_dict()
            }
            producer.publish(json.dumps(message), topic)
            print(f"📤 Sent row to Kafka: {message}")

        print(f"✅ Published all data for {data_type.value} to Kafka.")

    except Exception as e:
        print(f"❌ Error while publishing data for {data_type.value}: {e}")


def extract_and_publish(scraper, producer, data_types, is_league, prefix, topic):
    """
    Extracts data using the scraper and publishes it to Kafka.

    :param scraper: Instance of LaLigaScraper.
    :param producer: Instance of KafkaProducerFootballCloud.
    :param data_types: List of DataTypes to extract.
    :param is_league: Boolean indicating if the data is for leagues (True) or players (False).
    :param prefix: Prefix for the output file names (e.g., 'league' or 'player').
    """
    for index, data_type in enumerate(data_types):
        is_first = index == 0
        output_file = f"{prefix}_{data_type.name.lower()}_stats.csv"
        
        try:
            df = scraper.get_data(data_type, output_file=output_file, is_league=is_league, isFirst=is_first)
            print(df)
            publish_dataframe_to_kafka(producer, df, data_type, topic)
        except Exception as e:
            print(f"❌ Error occurred while processing {data_type.value}: {e}")



if __name__ == "__main__":


    driver = setup_driver()
    scraper = LaLigaScraper(driver)

    KAFKA_URL = "localhost"
    KAFKA_PORT = 9092
    KAFKA_TOPIC_ = "clasica_league"

    try:
        producer = KafkaProducerFootballCloud(KAFKA_URL, KAFKA_PORT)
        print("✅ Successfully connected to Kafka.")
    except KafkaError as e:
        print(f"❌ Error while connecting to Kafka: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

    print()

    data_types = [
        DataType.EFICIENCIA,
        # DataType.DISCIPLINA,
        # DataType.ATAQUES,
        # DataType.DEFENSIVA,
        # DataType.CLASICO
    ]

    try:
        # Extract and publish league data
        extract_and_publish(scraper, producer, data_types, is_league=True, prefix="league", topic="clasica_league")

        # Extract and publish player data
        # extract_and_publish(scraper, producer, data_types, is_league=False, prefix="player")

    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

    finally:
        driver.quit()
        print("WebDriver closed.")

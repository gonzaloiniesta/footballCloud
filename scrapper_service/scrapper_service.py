from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from technologics_classes import LaLigaScraper, DataType
from technologics_classes import KafkaProducerFootballCloud
from kafka.errors import KafkaError
from pandas import DataFrame

def setup_driver():
    options = Options()
    # options.add_argument('--headless')  # Descomentar para ejecutar sin interfaz gráfica
    driver_service = Service('/usr/bin/chromedriver')  # Ajusta la ruta si es necesario
    driver = webdriver.Chrome(service=driver_service, options=options)
    return driver

def remove_accents(text: str):
    """
    Remove accents from a given string.

    :param text (str): The input string with accented characters.
    """
    return text.encode('ascii', 'ignore').decode('utf-8')


def publish_dataframe_to_kafka(producer: KafkaProducerFootballCloud, df: DataFrame, data_type: DataType, topic: str, isLeague: bool):
    """
    Publishes each row of the DataFrame as a JSON message to a specified Kafka topic.

    :param producer: Instance of KafkaProducerFootballCloud used to send messages to Kafka.
    :param df: DataFrame containing the data to be sent. Each row is sent as a separate message.
    :param data_type: Enum value of type DataType representing the type of data being sent (e.g., Eficiencia, Disciplina).
    :param topic: The Kafka topic to which the messages will be published.
    :param isLeague: Boolean indicating if the data pertains to league statistics (True) or player statistics (False).
    
    The function iterates over each row in the DataFrame, converts the row to a dictionary, and sends it as a JSON message to Kafka.
    Depending on whether the data is for leagues or players, an appropriate key is generated and included in the message.
    """

    try:
        for _, row in df.iterrows():

            msg = row.to_dict()

            if isLeague:
                key = {
                    "team": remove_accents(str(msg["EQUIPO"])),
                    "stats": data_type.value
                }
            else:
                key = {
                    "player": msg["NOMBRE"],
                    "stats": data_type.value 
                }

            producer.publish(topic=topic, key=key, message=msg)

    except Exception as e:
        print(f"❌ Error while publishing data: {e}")


def extract_and_publish(scraper, producer, data_types, is_league, prefix, topic):
    """
    Extracts data using the scraper and publishes it to a specified Kafka topic.

    :param scraper: Instance of LaLigaScraper responsible for extracting data from the web.
    :param producer: Instance of KafkaProducerFootballCloud used to publish messages to Kafka.
    :param data_types: List of DataType enums representing the types of data to extract (e.g., Eficiencia, Disciplina).
    :param is_league: Boolean indicating if the data to be extracted is for leagues (True) or players (False).
    :param prefix: Prefix for the output CSV file names (e.g., 'league' or 'player').
    :param topic: The Kafka topic where the extracted data will be published.

    This function iterates over a list of data types, extracts the corresponding data using the scraper,
    and publishes the data to Kafka. Each type of data is saved to a CSV file with a specific name.
    """
    for index, data_type in enumerate(data_types):
        is_first = index == 0
        # output_file = f"{prefix}_{data_type.name.lower()}_stats.csv"
        
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
        DataType.DISCIPLINA,
        DataType.ATAQUES,
        DataType.DEFENSIVA,
        DataType.CLASICO
    ]

    try:
        # Extract and publish league data
        extract_and_publish(scraper, producer, data_types, is_league=True, prefix="league", topic="league_stats")

        # Extract and publish player data
        # extract_and_publish(scraper, producer, data_types, is_league=False, prefix="player", topic="player_stats")

    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

    finally:
        driver.quit()
        print("WebDriver closed.")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from technologics_classes.webScrapingClass import LaLigaScraper, DataType
from technologics_classes.kafkaProducerClass import KafkaProducerFootballCloud
import json

# Configuración del WebDriver de Selenium
def setup_driver():
    options = Options()
    # options.add_argument('--headless')  # Descomentar para ejecutar sin interfaz gráfica
    driver_service = Service('/usr/bin/chromedriver')  # Ajusta la ruta si es necesario
    driver = webdriver.Chrome(service=driver_service, options=options)
    return driver

# Función para publicar el DataFrame en Kafka
def publish_dataframe_to_kafka(producer, df, data_type):
    """
    Publica cada fila del DataFrame como un mensaje en Kafka.

    :param producer: Instancia de KafkaProducerFootballCloud.
    :param df: DataFrame de pandas con los datos a enviar.
    :param data_type: Tipo de datos (DataType Enum) para agregar metadatos.
    """
    for _, row in df.iterrows():
        message = {
            "data_type": data_type.value,
            "data": row.to_dict()
        }
        producer.publish(message)
    print(f"Published data for {data_type.value} to Kafka.")




if __name__ == "__main__":


    driver = setup_driver()
    scraper = LaLigaScraper(driver)

  
    KAFKA_URL = "localhost"
    KAFKA_PORT = 9092
    KAFKA_TOPIC = "football-data"

    producer = KafkaProducerFootballCloud(KAFKA_URL, KAFKA_PORT, KAFKA_TOPIC)

    try:
        
        # League Data
        df_efficiency = scraper.get_data(DataType.EFICIENCIA, output_file="league_efficiency_stats.csv", is_league=True, isFirst=True)
        publish_dataframe_to_kafka(producer, df_efficiency, DataType.EFICIENCIA)

        df_discipline = scraper.get_data(DataType.DISCIPLINA, output_file="league_discipline_stats.csv", is_league=True, isFirst=False)
        publish_dataframe_to_kafka(producer, df_discipline, DataType.DISCIPLINA)

        df_attacks = scraper.get_data(DataType.ATAQUES, output_file="league_attack_stats.csv", is_league=True, isFirst=False)
        publish_dataframe_to_kafka(producer, df_attacks, DataType.ATAQUES)

        df_defensive = scraper.get_data(DataType.DEFENSIVA, output_file="league_defensive_stats.csv", is_league=True, isFirst=False)
        publish_dataframe_to_kafka(producer, df_defensive, DataType.DEFENSIVA)

        df_classic = scraper.get_data(DataType.CLASICO, output_file="league_classic_stats.csv", is_league=True, isFirst=False)
        publish_dataframe_to_kafka(producer, df_classic, DataType.CLASICO)




        # Players Data
        df_efficiency = scraper.get_data(DataType.EFICIENCIA, output_file="player_efficiency_stats.csv", is_league=False, isFirst=True)
        publish_dataframe_to_kafka(producer, df_efficiency, DataType.EFICIENCIA)

        df_discipline = scraper.get_data(DataType.DISCIPLINA, output_file="player_discipline_stats.csv", is_league=False, isFirst=False)
        publish_dataframe_to_kafka(producer, df_discipline, DataType.DISCIPLINA)

        df_attacks = scraper.get_data(DataType.ATAQUES, output_file="player_attack_stats.csv", is_league=False, isFirst=False)
        publish_dataframe_to_kafka(producer, df_attacks, DataType.ATAQUES)

        df_defensive = scraper.get_data(DataType.DEFENSIVA, output_file="player_defensive_stats.csv", is_league=False, isFirst=False)
        publish_dataframe_to_kafka(producer, df_defensive, DataType.DEFENSIVA)

        df_classic = scraper.get_data(DataType.CLASICO, output_file="player_classic_stats.csv", is_league=False, isFirst=False)
        publish_dataframe_to_kafka(producer, df_classic, DataType.CLASICO)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()
        print("WebDriver closed.")

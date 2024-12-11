from integrations import KafkaConsumerFootballCloud

def imprime(k, v):
    print(f'Key: {k}, Value: {v}')

consumer = KafkaConsumerFootballCloud(
    kafka_url='localhost',
    kafka_port=9092,
    topic='league_stats',
    group_id='test_group_001'  # Cambia el group_id si es necesario
)

try:
    consumer.subscribe(imprime)
except Exception as e:
    print(f"❌ Error during subscription: {e}")

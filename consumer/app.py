import atexit

from confluent_kafka import Consumer, KafkaError

# Kafka broker configuration
kafka_config = {
    'bootstrap.servers': 'kafka-service.signalpet.svc.cluster.local:9092',
    'group.id': 'AIconsumer',
    'auto.offset.reset': 'earliest'
}

# Create Kafka consumer
consumer = Consumer(kafka_config)

# Subscribe to the topic
consumer.subscribe(['ImageToProcess'])

def shutdown_hook():
    # Close the consumer on exit
    print("Closing consumer")
    consumer.close()
    
atexit.register(shutdown_hook)

try:
    while True:
        msg = consumer.poll(timeout=5.0)  # Poll for messages
        if msg is None:
            print("No new messages")
            continue

        if msg.error():
            if msg.error().code() != KafkaError._PARTITION_EOF:
                print(msg.error())
            
            continue

        # Process the message (you can add your image analysis logic here)
        image_id = msg.value().decode('utf-8')
        #
        print(f"Received message: {image_id}")
        image = open(f"/app/uploaded_images/{image_id}.png")
        # TODO: AI model

except Exception as e:
    print(f"Failed to run consumer {e}")

from flask import Flask, request, jsonify
from flask_kafka import FlaskKafka
import uuid
import os
from queue import Queue
from flask_kafka import FlaskKafka

app = Flask(__name__)
app.config["KAFKA_CONFIG"] = {'bootstrap.servers': 'kafka-service.signalpet.svc.cluster.local:9092',
                              'group.id': 'AIproducer'}


bus = FlaskKafka()
bus.init_app(app)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    image_id = str(uuid.uuid4())
    image_path = f'uploaded_images/{image_id}.png'
    image_file.save(image_path)

    publisher = bus.get_producer()
    publisher.produce("ImageToProcess", image_id)
    publisher.poll(1)


    return jsonify({'success': True, 'image_id': image_id}), 200

if __name__ == '__main__':
    if not os.path.exists('uploaded_images'):
        os.makedirs('uploaded_images')
    bus.run()
    app.run(host='0.0.0.0', port=5000, debug=True)


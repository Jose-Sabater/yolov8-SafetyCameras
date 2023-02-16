from flask import Flask, request, jsonify
import numpy as np
from .inference import infere_image, load_model

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5555
API_PATH = "/api/inference"

app = Flask(__name__)

model = load_model()


@app.route(API_PATH, methods=["POST"])
def infer_image():
    # Get the image data from the POST request
    data = request.get_json()
    image_data = data.get("image")

    # Convert the image data to a numpy array
    image = np.array(image_data, model)

    # Run inference on the image
    results = infere_image(image)

    # Return the results as a JSON object
    return jsonify(results)


@app.route("/health", methods=["GET", "POST"])
def health():
    return {"status": "Im healthy"}


if __name__ == "__main__":
    app.run(host=SERVER_HOST, debug=True, port=SERVER_PORT)

import cv2
import numpy as np
from flask import Flask, jsonify

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 4000
API_PATH = "/api/img_capture"

app = Flask(__name__)

# Create a variable to store the most recent image
latest_image = None


# Define a function to continuosly read images from the webcam
def read_images():
    global latest_image
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            latest_image = frame


# Start a separate thread to read images continuosly
import threading

threading.Thread(target=read_images, daemon=True).start()


# Route that returns the most recent image as a json object when pinged
@app.route("/api/img", methods=["GET"])
def img_capture():
    global latest_image
    if latest_image is not None:
        return jsonify({"image": latest_image.tolist()})
    else:
        return {"Message": f"No image available {404}"}


@app.route("/health", methods=["GET", "POST"])
def health():
    return {"status": "I'm healthy"}


if __name__ == "__main__":
    app.run(host=SERVER_HOST, port=SERVER_PORT)

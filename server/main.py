"""Main module for the Flask server"""
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import numpy as np
from inference import infere_image, load_model
from utils import plot_bboxes
import base64
import matplotlib.pyplot as plt
import cv2
import time

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5555
API_PATH = "/api/inference"

app = Flask(__name__)
socketio = SocketIO(app)

model = load_model()


@app.route("/")
def index():
    return render_template("index.html")


@app.route(API_PATH, methods=["POST"])
def infer_image():
    """Run inference on the image data sent over the POST request
    and send the results back to the client over SocketIO
    """
    # Get the image data from the POST request
    data = request.get_json()
    image_data = data.get("image")

    # Convert the image data to a numpy array
    image = np.asarray(image_data)

    # Run inference on the image
    inf_img = infere_image(image, model)

    # # resize the image to 640 x 480
    # image = cv2.resize(image, (640, 480))

    # Mask the image
    results = plot_bboxes(
        image,
        inf_img[0].boxes.boxes,
        masks=inf_img[0].masks.masks,
        score=True,
        conf=0.6,
    )
    # save results img
    cv2.imwrite("results.jpg", results)

    start = time.time()
    _, im_arr = cv2.imencode(
        ".jpg", results
    )  # im_arr: image in Numpy one-dim array format.
    im_bytes = im_arr.tobytes()
    base64_img = base64.b64encode(im_bytes).decode("utf-8")
    end = time.time()
    print(end - start)

    # save image_data in txt file
    with open("image_data.txt", "w") as f:
        f.write(base64_img)

    # display the image
    #
    # Send the image data to the client over SocketIO
    socketio.emit("results", {"image": base64_img})

    return jsonify({"success": True})


@app.route("/health", methods=["GET", "POST"])
def health():
    """Health check endpoint for the server"""
    return {"status": "Im healthy"}


@socketio.on("connect")
def on_connect():
    print("Client connected")


@socketio.on("disconnect")
def on_disconnect():
    print("Client disconnected")


if __name__ == "__main__":
    socketio.run(app, host=SERVER_HOST, debug=True, port=SERVER_PORT)

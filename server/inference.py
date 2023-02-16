from ultralytics import YOLO


# Load a model
def load_model():
    model = YOLO("yolov8m-seg.pt")  # medium
    return model


def infere_image(image, model):
    results = model.predict(image)
    return results

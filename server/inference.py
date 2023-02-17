from ultralytics import YOLO
import numpy as np


# Load a model
def load_model():
    """Load a model from yolov8"""
    model = YOLO("yolov8m-seg.pt")  # medium
    return model


def infere_image(image: np.ndarray, model: YOLO) -> np.ndarray:
    """Run inference on the image
    Args:
        image (np.ndarray): image to run inference on
        model (YOLO): model to run inference on
        Returns:
        results (np.ndarray): results of inference
    """
    results = model.predict(image)
    return results

"""
Run a rest API exposing the yolov5s object detection model
"""
import argparse
import io
import os

import torch
from PIL import Image
from flask import Flask, request

app = Flask(__name__)

DETECTION_URL = "/v1/object-detection/yolov5s"
model_path = "./stickytraps.pt"


@app.route(DETECTION_URL, methods=["POST"])
def predict():
    if not request.method == "POST":
        return

    if request.files.get("image"):
        image_file = request.files["image"]
        image_bytes = image_file.read()

        img = Image.open(io.BytesIO(image_bytes))

        results = model(img, size=640)  # reduce size=320 for faster inference
        return results.pandas().xyxy[0].to_json(orient="records")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask API exposing YOLOv5 model")
    parser.add_argument("--port", default=33507, type=int, help="port number")
    args = parser.parse_args()

    model = torch.hub.load("ultralytics/yolov5", 'custom', path=model_path, force_reload=True)  # force_reload to recache
    #model = torch.hub.load("ultralytics/yolov5", "yolov5s", force_reload=True)
    #app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

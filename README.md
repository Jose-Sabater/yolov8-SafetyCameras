# yolov8-SafetyCameras

## Setup

Flask server on AWS functioning with some API endpoints. Receiving a flow of images, and doing inference using Yolo-v8.  
Then streaming them using a socket, into a Route53 endpoint.

Locally it's just a logi webcam capturing images. It is connected to a raspberry Pi, you can see the code in the repo. Runs Asynchronous.

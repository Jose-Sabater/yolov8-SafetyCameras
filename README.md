# yolov8-SafetyCameras

## Intro
This was a quick test to evaluate yolo-v8 and sending images to the cloud.

## Setup

Flask server on AWS functioning with some API endpoints. Recieving a flow of images, and doing inference using Yolo-v8.  
Then streaming them using a socket, into a Route53 endpoint.

Locally its just a logi webcam capturing images. It is connected to a rasperry pi, you can see the code in the repo. Runs Asynchronous.

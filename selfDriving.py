import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import time
from threading import Thread
from routing import routing

class cameraThread:
    def __init__(self, detector):
        # Start capturing video input from the camera
        self.cap = cv2.VideoCapture(0)
        self.detector = detector # object detection model
        self.detection_result = []

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.processImage, args=()).start()
        return self

    def processImage(self):
        # Continuously capture images from the camera and run inference
        while self.cap.isOpened():
            _, image = self.cap.read()
            image = cv2.flip(cv2.flip(image, 1), 0) # Added vertical flip because my camera mounted upside down
            # Convert the image from BGR to RGB as required by the TFLite model.
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # Create a TensorImage object from the RGB image.
            input_tensor = vision.TensorImage.create_from_array(rgb_image)
            # Run object detection estimation using the model.
            self.detection_result = self.detector.detect(input_tensor)

def initCameraThread():
    # Initialize the object detection model
    model = 'efficientdet_lite0.tflite'
    base_options = core.BaseOptions(file_name=model, use_coral=False, num_threads=3)
    detection_options = processor.DetectionOptions(max_results=3, score_threshold=0.6)
    options = vision.ObjectDetectorOptions(base_options=base_options, detection_options=detection_options)
    detector = vision.ObjectDetector.create_from_options(options)

    # create a thread dedicated to capturing images, processing them
    thread = cameraThread(detector).start()
    time.sleep(2.0)

    return thread

def main():
    thread = initCameraThread()

    origin = (49,0)
    destination = (7,48)
    stepsAfterStop = 15 # keeps track of how many moves car makes after stoping at stop sign

    while destination != None:
        for detection in thread.detection_result.detections:
            # stop car until person not detected
            if detection.categories[0].category_name == 'person':
                while len(thread.detection_result.detections) != 0 and 'person' in thread.detection_result.detections[0].categories[0].category_name:
                    time.sleep(0.1)

            # stop car for 5 seconds at stop sign
            if detection.categories[0].category_name == 'stop sign':
                stepsAfterStop += 1
                if stepsAfterStop > 15:
                    stepsAfterStop = 0
                    time.sleep(5)

        destination = routing(origin, destination) # route to destination
    thread.cap.release()

if __name__ == "__main__":
    main() 

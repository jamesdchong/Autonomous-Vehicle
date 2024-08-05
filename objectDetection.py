import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils
import time
from threading import Thread

class cameraThread:
    def __init__(self, detector):
        self.cap = cv2.VideoCapture(0) # Start capturing video input from the camera

        # set resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.frames = [] # image
        self.detector = detector # object detection model

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
            detection_result = self.detector.detect(input_tensor)
            # Draw keypoints and edges on input image, save as frame
            self.frames.append(utils.visualize(image, detection_result))

# Continually run inferences acquired from camera
def objectDetection():
    # Visualization parameters
    row_size = 20  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 255)  # red
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 20

    # Initialize the object detection model
    model = 'efficientdet_lite0.tflite'
    base_options = core.BaseOptions(file_name=model, use_coral=False, num_threads=3) # 1 thread used: main thread
    detection_options = processor.DetectionOptions(max_results=3, score_threshold=0.3)
    options = vision.ObjectDetectorOptions(base_options=base_options, detection_options=detection_options)
    detector = vision.ObjectDetector.create_from_options(options)

    # create a thread dedicated to capturing images, processing them
    thread = cameraThread(detector).start()
    time.sleep(2.0)

    # Variables to calculate FPS
    counter, fps = 0, 0
    start_time = time.time()

    while True:
        # get a frame processed by the thread
        if thread.frames:
            image = thread.frames.pop(0)

            # keeps track of frames processed
            counter += 1

        # Calculate the FPS
        if counter % fps_avg_frame_count == 0:
            end_time = time.time()
            fps = fps_avg_frame_count / (end_time - start_time)
            start_time = time.time()

        # Show the FPS
        fps_text = 'FPS = {:.1f}'.format(fps)
        text_location = (left_margin, row_size)
        cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN, font_size, text_color, font_thickness)
        
        # Display image
        cv2.imshow("objectDetection", image)

        # Stop the program if the ESC key is pressed
        if cv2.waitKey(1) == 27:
            break

    thread.cap.release()
    cv2.destroyAllWindows()

def main():
  objectDetection()

if __name__ == '__main__':
  main()
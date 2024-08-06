# Self-Driving Car made with Raspberry Pi

The autonomous vehicle employs an ultrasonic sensor that swivels to map its surroundings, effectively avoiding obstacles.

https://github.com/user-attachments/assets/f17980ab-5e5d-40ea-bce2-74d86e204139

An integrated camera utilizes object detection to identify stop signs and pedestrians.

![Stop](https://github.com/user-attachments/assets/1427dd51-f6ab-40cf-ad7b-f79aa0137494)
![Light](https://github.com/user-attachments/assets/66adfb58-57ab-4dba-aeed-8ca794344457)
![Dog](https://github.com/user-attachments/assets/4aa63e45-28c9-4e08-b43f-f47fe6bb79ac)

Leveraging the environmental mapping obtained via the ultrasonic sensor, the vehicle employs the A* algorithm to calculate the shortest path to a predetermined destination. This ensures the avoidance of obstacles, adherence to stop signs, and the pausing of movement until pedestrians are no longer in the path. The full self-driving capability integrates both object detection and routing. The A* algorithm is utilized for path creation, while multithreading is implemented using OpenCV (cv2) and TensorFlow inference.

https://github.com/user-attachments/assets/5459383e-f412-4e3d-adaf-3f1094f28ea7

Communication with the vehicle is managed through both Bluetooth and Wi-Fi, facilitated by a frontend Electron application that controls movement and displays vehicle statistics. On the server side, housed in a Raspberry Pi, data received via the web socket from the client directs vehicle movement based on the received inputs. Key metrics such as distance traveled, vehicle temperature, and battery status are converted to JSON format and sent to the client to update the application in real-time.
![UI](https://github.com/user-attachments/assets/5ed10b75-eb1a-4ec9-84cb-10bb8bf7c0f8)
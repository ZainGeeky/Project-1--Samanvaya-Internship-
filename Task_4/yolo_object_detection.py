import cv2
import numpy as np
import glob
import random

# Load Yolo
net = cv2.dnn.readNet("Task_4/yolov3_training_last.weights", "Task_4/yolov3_testing.cfg")

# Name custom object
classes = ["koala"]

# try:
#     # Load Yolo
#     net = cv2.dnn.readNet("Task_4/yolov3_training_last.weights", "Task_4/yolov3_testing.cfg")
#     # Rest of your code
# except Exception as e:
#     print("Error:", e)


# Images path
images_path = glob.glob(r"/Users/muhammedzainuddinmoosa/Desktop/Project-1--Samanvaya-Internship-/Task_4/images/*.jpg")

layer_names = net.getLayerNames()
output_layers_indices = net.getUnconnectedOutLayers()  # Get the indices of the output layers

print("Layer Names:", layer_names)
print("Output Layers Indices:", output_layers_indices)

# Get the names of the output layers
output_layers = []
for i in output_layers_indices:
    layer_name = layer_names[i - 1]
    output_layers.append(layer_name)

colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Insert here the path of your images
random.shuffle(images_path)

# loop through all the images
for img_path in images_path:
    # Loading image
    img = cv2.imread(img_path)
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.53:
                # Object detected
                print(class_id)
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    print(indexes)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 2)

    cv2.imshow("Image", img)
    key = cv2.waitKey(0)

cv2.destroyAllWindows()


import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
from PIL import Image

import cv2
from pyardrone.video import VideoClient
from pyardrone import ARDrone
import time

cap = VideoClient('192.168.1.1', 5555)
cap.connect()
cap.video_ready.wait()


drone = ARDrone()
drone.navdata_ready.wait()

sys.path.append("..")

from utils import label_map_util

from utils import visualization_utils as vis_util

MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90

#MODEL
opener = urllib.request.URLopener()
opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
tar_file = tarfile.open(MODEL_FILE)
for file in tar_file.getmembers():
    file_name = os.path.basename(file.name)
    if 'frozen_inference_graph.pb' in file_name:
        tar_file.extract(file, os.getcwd())

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')


label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


flag = 0
with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        while True:
            image_np = cap.frame
            image_np_expanded = np.expand_dims(image_np, axis=0)
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')
            (boxes, scores, classes, num_detections) = sess.run(
              [boxes, scores, classes, num_detections],
              feed_dict={image_tensor: image_np_expanded})
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=8)
            list = [category_index.get(value) for index,value in enumerate(classes[0]) if scores[0,index] > 0.5]

            print(list)
            for name in list:
                if name['name'] == 'bottle' or name['name'] == 'cup' and flag == 0:
                    flag = 1
                    print("starter object detected")
                    time.sleep(0.1)
                    while not drone.state.fly_mask:
                        drone.takeoff()

                    time.sleep(0.1)
                elif name['name'] == 'cell phone' or name['name'] == 'remote' or name['name'] == 'skateboard' or name['name'] == 'surfboard':
                    while drone.state.fly_mask:
                        drone.land()
                        print("lander object detected")
                        flag = 0
                if name['name'] == 'cup':

                    posY =( boxes[0][0][0]  +  boxes[0][0][2])/2
                    posX =( boxes[0][0][1]  +  boxes[0][0][3])/2
                    print('Position y' , posY)
                    print('Position x' , posX)

                    #print(boxes[0])

                    if posX < 0.2:
                        print("very left")
                        drone.move(ccw = 1.0)
                    elif posX < 0.4:
                        print("left")
                        drone.move(ccw = 0.5)
                    elif posX <= 0.60 and posX >= 0.4:
                        print("middle")
                        drone.move(forward = 1)
                    elif posX > 0.60:
                        print("right")
                        drone.move(cw = 0.5)
                    elif posX > 0.80:
                        print("very right")
                        drone.move(cw = 1.0)



            cv2.imshow('object detection', cv2.resize(image_np, (800,600)))
            if cv2.waitKey(25) & 0xFF == ord('q'):
                while drone.state.fly_mask:
                    drone.land()
                cv2.destroyAllWindows()
                break

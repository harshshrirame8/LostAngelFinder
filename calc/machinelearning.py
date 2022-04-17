
import numpy as np
import cv2
import sklearn
import pickle
from django.conf import settings
import os
from keras.models import model_from_json
import json


STATIC_DIR = settings.STATIC_DIR
print("----------------------------------" , STATIC_DIR)

face_detector_model = cv2.dnn.readNetFromCaffe(os.path.join(STATIC_DIR , 'models/deploy.prototxt.txt'),
                                               os.path.join(STATIC_DIR ,'models/res10_300x300_ssd_iter_140000.caffemodel'))
model_file = open(os.path.join(STATIC_DIR , 'models/better_model.json'), "r")
model_json = model_file.read()
model = model_from_json(model_json)
model.load_weights(os.path.join(STATIC_DIR , 'models/better_model_weights.h5'))

def predictor(image):
    IMAGE_SHAPE = (224, 224)
    IMAGE_SHAPE+(3,)
    img_resize = cv2.resize(image , IMAGE_SHAPE)
    predicted = model.predict(np.array([img_resize]))
    ind = np.argmax(predicted , axis = 1)
    index = ind[0]
    return index

def pipeline_model(path):
    # pipeline model
    img = cv2.imread(path)
    image = img.copy()
    h,w = img.shape[:2]
    # face detection
    img_blob = cv2.dnn.blobFromImage(img,1,(300,300),(104,177,123),swapRB=False,crop=False)
    face_detector_model.setInput(img_blob)
    detections = face_detector_model.forward()
    
    # machcine results
    machinlearning_results = dict(face_detect_score = [], 
                                 face_name = [],
                                 face_name_score = [],
                                 emotion_name = [],
                                 emotion_name_score = [],
                                 count = [])
    count = 1
    if len(detections) > 0:
        for i , confidence in enumerate(detections[0,0,:,2]):
            if confidence > 0.5:
                box = detections[0,0,i,3:7]*np.array([w,h,w,h])
                startx,starty,endx,endy = box.astype(int)
                cropped = image[starty:endy , startx:endx]
                #Detected Face in Cropped Variable................................

                cnt = predictor(image)
                print("YYYYYYYYYYYYYYAAAAAAAAAAAAAYYYYYYYYYYYYYYY -- " , cnt)
                break            
    return cropped , cnt






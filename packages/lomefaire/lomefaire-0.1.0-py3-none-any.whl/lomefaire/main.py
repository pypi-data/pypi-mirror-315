import cv2
import numpy as np

def hello_lib():
    print('Hello, world!')
    img = np.zeros((9,9,3), dtype=np.uint8)
    img = cv2.circle(img, (4,4), 3, (255,255,255), -1)
    print(img[:,:,0])
    
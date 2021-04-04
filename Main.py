import threading
import time
import cv2
import numpy as np
import imutils
import serial


class videoStream:
    cam = cv2.VideoCapture(0)
    frame = np.empty([480, 640, 3])
    displayFrame = True
    exit = False
    location = [200,150]
    faceInCam = False
    tracking = True
    autoOff = True
    frameCount = 1


def captureVid():
    while True:
        if(obj.displayFrame):
            ret, frame = obj.cam.read()
            obj.frame = frame
            obj.frameCount = (obj.frameCount + 1) % 150
        else:
            obj.frame = np.empty([480, 640, 3])
        print(obj.frameCount, obj.faceInCam)
        
        cv2.imshow('frame', obj.frame)
        key = cv2.waitKey(1)
        if (key == ord('q')): 
            obj.exit = True
            obj.cam.release()
            ser.close()
            cv2.destroyAllWindows()
            break
        elif(key == ord('a')):
            obj.displayFrame = True
        elif(key == ord('s')):
            obj.autoOff = False
            if(obj.tracking):
                obj.tracking = False
            else:
                obj.tracking = True
        elif(key == ord(" ")):
            obj.tracking = False
            obj.location = [200, 150]
            obj.autoOff = False
        elif(key == ord("z")):
            if(obj.autoOff):
                obj.autoOff = False
            else:
                obj.autoOff = True
        
def faceSearch():
    while True:
        if(obj.exit):
            break
        if(obj.frameCount > 100):
            if(obj.faceInCam):
                obj.faceInCam = False
            else:
                obj.displayFrame = False
                obj.frameCount = 1
        else:
            time.sleep(1)
        

def recogFace():
    net = cv2.dnn.readNetFromCaffe("./deploy.prototxt.txt", "./res10_300x300_ssd_iter_140000.caffemodel")
    time.sleep(2)
    while True:
        if(obj.exit):
            break
        if(obj.tracking and obj.frameCount % 3 == 0):
            frame = obj.frame
            frame = imutils.resize(frame, width=400)
            (h, w) = frame.shape[:2]
            try:
                blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
            except:
                continue
            net.setInput(blob)
            detections = net.forward()
            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence < 0.5:
                    continue
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                print(startX, endX, startY, endY)
                obj.faceInCam = True
                obj.location = [(startX + endX)/2, ((startY + endY)/2)]
                if(obj.location[0] > 400 or obj.location[1] > 300):
                    continue
                s = str(int(obj.location[0])) + "|" + str(int(obj.location[1])) + "\n"
                print(s)
                ser.write(s.encode())

if __name__ == "__main__":
    ser = serial.Serial('COM5', 9600, timeout=0.1)
    obj = videoStream()
    p1 = threading.Thread(target=captureVid)
    p2 = threading.Thread(target=faceSearch)
    p3 = threading.Thread(target=recogFace)
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()

"""
Code responsible for Face recognition, Arduino Communication, Video Capture and Video Display
"""

import threading
import time
import cv2
import numpy as np
import serial
import mediapipe as mp
import sqlite3 as sq3


class videoStream:
    cam = cv2.VideoCapture(0)
    frame = np.empty([480, 640, 3])
    displayFrame = True
    exit = False
    location = [200, 150]
    faceInCam = False
    tracking = True
    autoOff = True
    frameCount = 1
    default = 0


def updateVal():
    connection = sq3.connect("Parameters.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM parameters")

    while True:
        time.sleep(0.5)
        test = cursor.fetchall()

        if test[0][1] == 0:
            obj.tracking = False
            obj.autoOff = False
        else:
            obj.tracking = True

        if test[1][1] == 0:
            obj.autoOff = False
        else:
            obj.autoOff = True

        if test[2][1] == 0:
            obj.displayFrame = False
        else:
            obj.displayFrame = True

        if test[3][1] == 0:
            obj.default = False
        else:
            obj.default = True


def captureVid():
    while True:
        if obj.displayFrame:
            ret, frame = obj.cam.read()
            obj.frame = frame
            obj.frameCount = (obj.frameCount + 1) % 150
        else:
            obj.frame = np.empty([480, 640, 3])
        # print(obj.frameCount, obj.faceInCam)
        
        cv2.imshow('frame', obj.frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            obj.exit = True
            obj.cam.release()
            ser.close()
            cv2.destroyAllWindows()
            break
        elif key == ord('a'):
            obj.displayFrame = True
        elif key == ord('s'):
            obj.autoOff = False
            if obj.tracking:
                obj.tracking = False
            else:
                obj.tracking = True
        elif key == ord(" "):
            obj.tracking = False
            obj.location = [200, 150]
            obj.autoOff = False
        elif key == ord("z"):
            if obj.autoOff:
                obj.autoOff = False
            else:
                obj.autoOff = True
        

def faceSearch():
    while True:
        if obj.exit:
            break
        if obj.frameCount > 100 and obj.autoOff:
            if obj.faceInCam:
                obj.faceInCam = False
            else:
                obj.displayFrame = False
            obj.frameCount = 1
        else:
            time.sleep(1)
        

def recogFace():
    time.sleep(2)
    mp_face_mesh = mp.solutions.face_mesh
    with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
        while True:
            if obj.exit:
                break
            if obj.tracking:
                try:
                    image = obj.frame
                    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False
                    results = face_mesh.process(image)
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    if results.multi_face_landmarks:
                        avgX = 0
                        avgY = 0
                        num = 0
                        for face_landmarks in results.multi_face_landmarks:
                            for landmark in face_landmarks.landmark:
                                x = landmark.x
                                y = landmark.y
                                num = num + 1
                                shape = image.shape
                                # print(shape)
                                relative_x = int(x * shape[1])
                                relative_y = int(y * shape[0])
                                avgX = avgX + relative_x
                                avgY = avgY + relative_y
                        avgX = int(avgX / num)
                        avgY = int(avgY / num)
                        if avgX > 640 or avgX < 0 or avgY > 480 or avgY < 0:
                            continue
                        obj.location[0] = avgX
                        obj.location[1] = avgY
                        obj.faceInCam = True
                        s = str(int(obj.location[0])) + "|" + str(int(obj.location[1])) + "\n"
                        print(s)
                        ser.write(s.encode())
                except Exception as e:
                    # print(e)
                    continue


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

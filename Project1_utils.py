# 201433264 Park Seong Won #
# Selfi-Rone Project # 

from djitellopy import Tello
import numpy as np
import time
import cv2

# Connect and Initialize the tello 
def intializeTello():
    myDrone = Tello()
    myDrone.connect()
    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0
    print('Battery : ', myDrone.get_battery())
    myDrone.streamoff()
    myDrone.streamon()
    return myDrone

# Get the image from the tello
def telloGetFrame(myDrone,w=640,h=480):   
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame, (w, h))
    return img

# Return the center points of the recognized face (center x, center y)
def findFace(img, width, height):
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)
    # List for finding close face only
    myFaceListCenter = []
    myFaceListArea = []
    # Detection image coordinate settings
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 225), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        myFaceListCenter.append([cx, cy])
        myFaceListArea.append(area)
    # Only return the coordinates of the close face
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        print('Coordinate : ', myFaceListCenter[i])
        print('Area :', myFaceListArea[i])
        return img, [myFaceListCenter[i], myFaceListArea[i]]
    else:
        return img, [[0,0], 0]

def findBody(img, width, height) :
    bodyCascade = cv2.CascadeClassifier("haarcascade_fullbody.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bodies = bodyCascade.detectMultiScale(imgGray, 1.1, 4)
    # List for finding close body only
    myBodyListCenter = []
    myBodyListArea = []
    # Detection image coordinate settings
    for (x, y, w, h) in bodies:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 225), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        myBodyListCenter.append([cx, cy])
        myBodyListArea.append(area)
    # Only return the coordinates of the close body
    if len(myBodyListArea) != 0:
        i = myBodyListArea.index(max(myBodyListArea))
        print('Coordinate : ', myBodyListCenter[i])
        print('Area :', myBodyListArea[i])
        return img, [myBodyListCenter[i], myBodyListArea[i]]
    else:
        return img, [[0,0], 0]

# To find a face, move back and see the wide scene
def randomMoving (myDrone) :
    myDrone.move_back(20)
    print('Move back 20cm complete!')

# Define the Selfi-Mode threshold value 
def selfiMode (myDrone, w=640, h=480) :
    print('Flight with a selfie mode')
    count = 0
    while (count < 30) :
        img = telloGetFrame(myDrone)
        img, info = findFace(img, w, h)
        # Print X,Y coordinates
        print('(X, Y) : ', info[0][:])
        # Print Bounding box area
        print('Area : ', info[1])
        if (info[1] == 0) :
            print('Recognization Failed!')
            randomMoving (myDrone)
            count = count + 1
        else : 
            if (info[0][0] <= 270) :
                myDrone.move_left(20)
                print('Move Left')
            if (info[0][0] >= 380) :
                myDrone.move_right(20)
                print('Move Right')
            if (info[0][1] <= 180) :
                myDrone.move_up(20)
                print('Move Up')
            if (info[0][1] >= 290) :
                myDrone.move_down(20)
                print('Move Down')
            if  (270<info[0][0]<380) and (180<info[0][1]<290):
                # Using area of rectangular, decide whether forward or backward
                if (info[1] < 45000):
                    myDrone.move_forward(20)
                    print('Move Forward')
                # To shot photoes every 1 second, total 5 phtoes
                else :  
                    print('Smile!')  
                    myFrame = myDrone.get_frame_read()
                    myFrame = myFrame.frame
                    cv2.imwrite('Selfi_Mode/Selfi_Mode_img_1.jpg', myFrame)
                    time.sleep(1)
                    myFrame = myDrone.get_frame_read()
                    myFrame = myFrame.frame
                    cv2.imwrite('Selfi_Mode/Selfi_Mode_img_2.jpg', myFrame)
                    time.sleep(1)
                    myFrame = myDrone.get_frame_read()
                    myFrame = myFrame.frame
                    cv2.imwrite('Selfi_Mode/Selfi_Mode_img_3.jpg', myFrame)
                    time.sleep(1)
                    myFrame = myDrone.get_frame_read()
                    myFrame = myFrame.frame
                    cv2.imwrite('Selfi_Mode/Selfi_Mode_img_4.jpg', myFrame)
                    time.sleep(1)
                    myFrame = myDrone.get_frame_read()
                    myFrame = myFrame.frame
                    cv2.imwrite('Selfi_Mode/Selfi_Mode_img_5.jpg', myFrame)
                    myDrone.move_back(20)
                    myDrone.move_back(20)
                    myDrone.flip("b")
                    print('Done!')
                    break             

# Define the Half-Mode threshold value 
def halfMode (myDrone, w=640, h=480) :
    print('Flight with a half mode')
    count = 0
    while (count < 30) :
        img = telloGetFrame(myDrone)
        img, info = findFace(img, w, h)
        # Print X,Y coordinates
        print('(X, Y) : ', info[0][:])
        # Print Bounding box area
        print('Area : ', info[1])
        if (info[1] == 0) :
            print('Recognization Failed!')
            randomMoving (myDrone)
            count = count + 1
            print('\nCount : ', count)
        # Find a suitable coordinate
        else : 
            if (info[0][0] <= 260) :
                myDrone.move_left(20)
            if (info[0][0] >= 370) :
                myDrone.move_right(20)
            if (info[0][1] <= 200) :
                myDrone.move_up(20)
            if (info[0][1] >= 250) :
                myDrone.move_down(20)
            if  (260<info[0][0]<370) and (200<info[0][1]<250):
                if (info[1] < 16000) :
                    myDrone.move_forward(20)
                # Using area of rectangular, decide whether forward or backward
                elif (info[1] > 40000) :
                    myDrone.move_back(20)
                # To shot photoes every 1 second, total 5 phtoes
                else :  
                    print('Smile!')
                    myFrame = myDrone.get_frame_read()
                    myFrame = myFrame.frame
                    cv2.imwrite('Half_Mode/Half_Mode_img_1.jpg', myFrame)
                    time.sleep(1)
                    myFrame = myDrone.get_frame_read()
                    myFrame = myFrame.frame
                    cv2.imwrite('Half_Mode/Half_Mode_img_2.jpg', myFrame)
                    time.sleep(1)
                    myFrame = myDrone.get_frame_read()
                    myFrame = myFrame.frame
                    cv2.imwrite('Half_Mode/Half_Mode_img_3.jpg', myFrame)
                    time.sleep(1)
                    myFrame = myDrone.get_frame_read()
                    myFrame = myFrame.frame
                    cv2.imwrite('Half_Mode/Half_Mode_img_4.jpg', myFrame)
                    time.sleep(1)
                    myFrame = myDrone.get_frame_read()
                    myFrame = myFrame.frame
                    cv2.imwrite('Half_Mode/Half_Mode_img_5.jpg', myFrame)
                    myDrone.flip("b")
                    print('Done!')
                    break

# Define the Full-Mode threshold value 
def fullMode (myDrone, w=640, h=480) :
    print('Flight with a full mode')
    count = 0
    myDrone.move_up(30)
    while (count < 45) :
        img = telloGetFrame(myDrone)
        img, info = findFace(img, w, h)
        # Print X,Y coordinates
        print('(X, Y) : ', info[0][:])
        # Print Bounding box area
        print('Area : ', info[1])
        if (info[1] == 0) :
            print('Recognization Failed!')
            randomMoving (myDrone)
            count = count + 1
            print('\nCount : ', count)
        # Find a suitable coordinate
        else : 
            if (info[0][0] <= 100) :
                myDrone.move_left(20)
            if (info[0][0] >= 540) :
                myDrone.move_right(20)
            if (info[0][1] <= 180) :
                myDrone.move_up(20)
            if (info[0][1] >= 380) :
                myDrone.move_down(20)
            if  (100<info[0][0]<540) and (180<info[0][1]<380):
                # Using area of rectangular, decide whether forward or backward
                if (info[1] < 500) :
                    myDrone.move_forward(20)
                elif (info[1] > 4000) :
                    myDrone.move_back(20)
                # To shot photoes every 1 second, total 5 phtoes
                else :  
                    print('Smile!')
                    myFrame = myDrone.get_frame_read()
                    myFrame = myFrame.frame
                    cv2.imwrite('Full_Mode/Full_Mode_img_1.jpg', myFrame)
                    time.sleep(1)
                    myFrame = myDrone.get_frame_read()
                    myFrame = myFrame.frame
                    cv2.imwrite('Full_Mode/Full_Mode_img_2.jpg', myFrame)
                    time.sleep(1)
                    myFrame = myDrone.get_frame_read()
                    myFrame = myFrame.frame
                    cv2.imwrite('Full_Mode/Full_Mode_img_3.jpg', myFrame)
                    time.sleep(1)
                    myFrame = myDrone.get_frame_read()
                    myFrame = myFrame.frame
                    cv2.imwrite('Full_Mode/Full_Mode_img_4.jpg', myFrame)
                    time.sleep(1)
                    myFrame = myDrone.get_frame_read()
                    myFrame = myFrame.frame
                    cv2.imwrite('Full_Mode/Full_Mode_img_5.jpg', myFrame)
                    myDrone.flip("b")
                    print('Done!')
                    break
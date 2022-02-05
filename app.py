import cv2
import numpy as np


frameWidth = 1280
frameHeight = 720
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)  # Width 
cap.set(4, frameHeight)  # Height
cap.set(10, 150)  # Brightness


myColors = [[0,177,69,40,255,255],
            [56,112,0,142,255,255],
            [131,97,0,179,255,255]]

myColorsValues = [[51, 153, 255],
                  [255, 0, 0],
                  [255, 0, 255]]

myPoints = [] # [x, y, colorId]



# To detect the colours
def findColor(img, myColors, myColorsValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y = getContours(mask)
        #cv2.imshow(str(color[0]), mask)
        cv2.circle(imgResult, (x,y), 10, myColorsValues[count], cv2.FILLED)
        if x!= 0 and y!=0:
            newPoints.append([x,y,count])
        count +=1
    return newPoints
    
    
    
# To get the contours
def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # img file should be binary only
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            #cv2.drawContours(imgResult, cnt, -1, (255,0,0), 3)
            peri = cv2.arcLength(cnt, True)   # Helps to approximate the corners of the shapes
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)  # Returns the corner points
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2, y



# To draw on video
def drawOnCanvas(myPoints, myColorsValues):
    for points in myPoints:
        cv2.circle(imgResult, (points[0],points[1]), 10, myColorsValues[points[2]], cv2.FILLED)
        cv2.circle(imgStatic, (points[0],points[1]), 10, myColorsValues[points[2]], cv2.FILLED)
    

imgStatic = np.zeros((720,1280,3))


while True:
    _, frame = cap.read()
    imgResult = frame.copy()  
    newPoints = findColor(frame, myColors, myColorsValues)
    if len(newPoints)!= 0 :
        for newP in newPoints:
            myPoints.append(newP)
    
    if len(myPoints)!= 0 :
        drawOnCanvas(myPoints, myColorsValues)
    
    cv2.imshow("Video", imgResult)
    cv2.imshow("Image", imgStatic)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

cv2.imwrite("Result/draw.jpg", imgStatic)
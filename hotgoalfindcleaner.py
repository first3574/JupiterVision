import cv2
import numpy as np
import logging
import nt_client
import ocupus_cam

cap=cv2.VideoCapture(r"D:\Infared Test Videos\Infrared-7-2014-04.mkv.avi")

#client = nt_client.NetworkTableClient("3574", True)
#client.setValue("/Vision/Test", "howdy")

vertTopLeftX = 0
vertTopLeftY = 0
horizBottomRightX = 0
horizBottomRightY = 0
x2 = 0
y2 = 0

while True:
    r,f=cap.read()
    f = cv2.resize(f,(320,240))
    gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)

    contourCount = 0

    verAndHorClose = False

    closeX = vertTopLeftX - horizBottomRightX
    closeY = horizBottomRightY - vertTopLeftY 

    if (closeX < 25 and closeY < 25 and closeX + closeY != 0) :
        verAndHorClose = True
    else :
        verAndHorClose = False

    (thresh, im_bw) = cv2.threshold(gray,200,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imshow("im_bw",im_bw)
    (contours, hierarchy) = cv2.findContours(im_bw,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    c = len(contours)

    for j in range(0, len(contours)) :
        cnt = contours[j]

        perimeter = cv2.arcLength(cnt,True)

        approx = cv2.approxPolyDP(cnt,0.01*perimeter,True)

        area = cv2.contourArea(cnt)

        if (area < 15 or perimeter < 7) :
            continue
        if (area < 25 or perimeter < 10) :
            continue
        if (perimeter > area * 2) :
            continue
        if (area > 10000 or perimeter > 1000) :
            continue
        if (perimeter + area > 10000) :
            continue

        x,y,w,h = cv2.boundingRect(cnt)

        areaApprox = cv2.contourArea(approx)

        if (h > 200 or w > 200) :
            continue
        if (areaApprox * 2 < area) :
            continue
        if (w == h) :
            continue

        ratio = (w * 1.0)/(h * 1.0)
        
        if (ratio > 0.4 and ratio < 3.0) :
            continue

        rect = cv2.minAreaRect(cnt)
        box = cv2.cv.BoxPoints(rect)
        box = np.int0(box)
        im = cv2.drawContours(f,[box],0,(0,0,255),2)
        img = cv2.rectangle(f,(x,y),(x+w,y+h),(255,0,0),2)

        if (w < h) : # vertical - yellow
            cv2.drawContours(f, [approx], -1, (0,255,255),3)
            contourCount += 1

            vertTopLeftX = x
            vertTopLeftY = y
            vertBottomRightX = x + w
            vertBottomRightY = y + h
            vertWidth = w
            vertHeight = h
            x1,y1,w1,h1 = x,y,w,h

            contour1 = j
            vertical1 = True

        elif (h < w) : # horizontal - cyan
            cv2.drawContours(f, [approx], -1, (255,255,0),3)
            contourCount += 1

            horizTopLeftX = x
            horizTopLeftY = y
            horizBottomRightX = x + w
            horizBottomRightY = y + h
            horizWidth = w
            horizHeight = h
            x2,y2,w2,h2 = x,y,w,h

            contour2 = j
            horizantal2 = True

        else :
            cv2.drawContours(f, [approx], -1, (0,255,0),3)
            contour3 = j
            wrong3 = True
            
        M = cv2.moments(cnt)
        if (M['m00'] != 0) :
            centroid_x = int(M['m10']/M['m00'])
            centroid_y = int(M['m01']/M['m00'])
            cv2.circle(f, (centroid_x, centroid_y), 1, (77, 177, 77), 5)
            cv2.circle(f, (x, y), 1, (177, 77, 177), 5)

    #client.setValue("/Vision/Vertical_And_Horizontal_Close", verAndHorClose)
    
    cv2.imshow("gray",gray)
    cv2.imshow("f",f)
    cv2.waitKey(1)

            
        

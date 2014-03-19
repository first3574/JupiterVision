import cv2
import numpy as np
import logging
import nt_client
import ocupus_cam

#cap=cv2.VideoCapture
cap=cv2.VideoCapture(2)

client = nt_client.NetworkTableClient("3574")
client.setValue("/Vision/Test", "howdy")

vertTopLeftX = 0
vertTopLeftY = 0
horizBottomRightX = 0
horizBottomRightY = 0

while True:
    r,f=cap.read()
    f = cv2.resize(f,(320,240))
    gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)

    contourCount = 0

    verAndHorClose = False
    logging.warning(str(vertTopLeftX) + "," + str(vertTopLeftY) + " (vertTopLeftX),(vertTopLeftY) Log")
    logging.warning(str(horizBottomRightX) + "," + str(horizBottomRightY) + " (horizBottomRightX),(horizBottomRightY) Log")
    closeX = vertTopLeftX - horizBottomRightX
    closeY = horizBottomRightY - vertTopLeftY 
    logging.warning(str(closeX) + "," + str(closeY) + " (closeX),(closeY) Log")
    if (closeX < 25 and closeY < 25 and closeX + closeY != 0) :
        verAndHorClose = True
    else :
        verAndHorClose = False
    
    (thresh, im_bw) = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
    (contours, hierarchy) = cv2.findContours(im_bw,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(f, contours, -1, (0,255,0),3)

    c = len(contours)
    #cv2.putText(f,c,(5,25), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0))
    
    for j in range(0, len(contours)) :
        cnt = contours[j]
        
        perimeter = cv2.arcLength(cnt,True)
        logging.warning(str(perimeter) + " perimeter Log")

        approx = cv2.approxPolyDP(cnt,0.01*perimeter,True)
        #logging.warning(str(j) + " x Log")
        #logging.warning(str(len(cnt)) + " Len cnt")
        
        area = cv2.contourArea(cnt)
        logging.warning(str(area) + " area Log")
        
        if (area < 40 or perimeter < 10) :
            continue
        if (perimeter > area) :
            continue
        if (area > 10000 or perimeter > 1000) :
            continue
        if (perimeter + area > 10000) :
            continue
        
        k = cv2.isContourConvex(cnt)
        logging.warning(str(k) + " k Log")

        x,y,w,h = cv2.boundingRect(cnt)
        
        areaApprox = cv2.contourArea(approx)
        #areaIm = cv2.contourArea(im)
        if (h > 200 or w > 200) :
            continue
        if (areaApprox * 2 < area) :
            continue
        if (w == h) :
            continue
        #if (k == True) :
            #continue

        rect = cv2.minAreaRect(cnt)
        box = cv2.cv.BoxPoints(rect)
        box = np.int0(box)
        im = cv2.drawContours(f,[box],0,(0,0,255),2)
        img = cv2.rectangle(f,(x,y),(x+w,y+h),(255,0,0),2)

        logging.warning(str(w) + " w Log")
        logging.warning(str(h) + " h Log")
        logging.warning(str(w * h) + " Blue area Log")
        logging.warning(str((h * 2) + (w * 2)) + " Blue perimeter Log")

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
        
            #if (0 < (w / h) < (32 / 32)) :
            contour1 = j
            vertical1 = True
            #client.setValue("/Vision/contour1", contour1 * 1.0)
            
            logging.warning(str(x) + ", " + str(y) + " (x, y) Log")
            logging.warning(str(j) + " j Log")
            logging.warning(str(k) + " k Log")
            logging.warning(str(len(cnt)) + " Len cnt")
            logging.warning(str(perimeter) + " perimeter Log")
            logging.warning(str(area) + " area Log")
            logging.warning("contour 1 " + str(contour1))
            logging.warning("contour 1 vertical " + str(vertical1))
           
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
            
            #if (0 < (w / h) < (32 / 32)) :
            contour2 = j
            horizantal2 = True
            
            logging.warning(str(x) + ", " + str(y) + " (x, y) Log")
            logging.warning(str(j) + " j Log")
            logging.warning(str(k) + " k Log")
            logging.warning(str(len(cnt)) + " Len cnt")
            logging.warning(str(perimeter) + " perimeter Log")
            logging.warning(str(area) + " area Log")
            logging.warning("contour 2 " + str(contour2))
            logging.warning("contour 2 horizantal " + str(horizantal2))
      
        else :
            cv2.drawContours(f, [approx], -1, (0,255,0),3)
            contour3 = j
            wrong3 = True

            logging.warning(str(j) + " j Log")
            logging.warning(str(k) + " k Log")
            logging.warning(str(len(cnt)) + " Len cnt")
            logging.warning(str(perimeter) + " perimeter Log")
            logging.warning(str(area) + " area Log")
            logging.warning("contour 3 " + str(contour3))
            logging.warning("contour 3 wrong " + str(wrong3))

        logging.warning(str(c) + " c Log")
        logging.warning(str(im) + " im Log")
        logging.warning(str(img) + " img Log")

        M = cv2.moments(cnt)
        if (M['m00'] != 0) :
            centroid_x = int(M['m10']/M['m00'])
            centroid_y = int(M['m01']/M['m00'])
            cv2.circle(f, (centroid_x, centroid_y), 1, (77, 177, 77), 5)
            cv2.circle(f, (x, y), 1, (177, 77, 177), 5)
            #cv2.circle(f, center, radius, color[, thickness[, lineType[, shift]]]) 

    #rect = cv2.minAreaRect(cnt)
    #box = cv2.cv.boxPoints(rect)
    #box2 = np.int0(box)
    #im = cv2.drawContours(f,[box2],0,(0,0,255),2)
    logging.warning(str(contourCount) + " contourCount Log")
    if (contourCount == 2) :
        logging.warning(str(x1) + ", " + str(y1) + " (x1, y1) Log")
        logging.warning(str(x2) + ", " + str(y2) + " (x2, y2) Log")
        x2BottomRight = x2 + w2
        y2BottomRight = y2 + h2
        cv2.line(f, (x1, y1), (x2 + w2, y2 + h2), (107,7,255))
        logging.warning(str(x1 - x2) + "," + str(y1 - y2) + " (x1 - x2),(y1 - y2) Log")
        cv2.rectangle(f,(x1, y1),(x2 + w2, y2 + h2),(255,7,107),2)
        logging.warning("x,y:x,y   "
                    + str(vertTopLeftX) + ","
                    + str(vertTopLeftY) + ":"
                    + str(horizBottomRightX) + ","
                    + str(horizBottomRightY))
        cv2.circle(f, (vertTopLeftX, vertTopLeftY), 1, (0, 127, 0), 5)
        cv2.circle(f, (horizBottomRightX, horizBottomRightY), 1, (0, 255, 0), 5)
    elif (contourCount != 2) :
        horizTopLeftX = 0
        horizTopLeftY = 0
        horizBottomRightX = 0
        horizBottomRightY = 0
        horizWidth = 0
        horizHeight = 0

    # send the contour count to the network tables
    client.setValue("/Vision/Vertical_And_Horizontal_Close", verAndHorClose)
    logging.warning(str(verAndHorClose) + " Vertical_And_Horizontal_Close")
    
    cv2.imshow("gray",gray)
    cv2.imshow("im_bw",im_bw)
    cv2.imshow("f",f)
    cv2.waitKey(1)
    
    #logging.warning('You smell haha get on my level')

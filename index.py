import numpy as np
import cv2

def center(x,y,w,h):
    x1 = int(w/2);
    y1 = int(h/2);
    cx = x+ x1;
    cy = y + y1;
    return cx,cy


cap = cv2.VideoCapture("1.mp4");

fgbg = cv2.createBackgroundSubtractorMOG2();
post =150;
offset =30;

xy1 = (20,post);
xy2 = (300,post);
detects = [];
total =0;
up=0;
down =0;

while 1:
    ret, frame = cap.read();

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY);
    fgmask = fgbg.apply(gray);
    retval, th = cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY);
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5));
    opening = cv2.morphologyEx(th,cv2.MORPH_OPEN,kernel,iterations=2);
    dilation = cv2.dilate(opening,kernel,iterations=8);
    closing = cv2.morphologyEx(dilation,cv2.MORPH_CLOSE,kernel,iterations=8);
    contours, hierarchy = cv2.findContours(closing,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE);
    i=0;

    cv2.line(frame,xy1,xy2,(255,0,0),3);
    cv2.line(frame,(xy1[0],post-offset),(xy2[0],post-offset),(255,255,0),2);
    cv2.line(frame,(xy1[0],post+offset),(xy2[0],post+offset),(255,255,0),2);
    for cnt in contours:
        (x,y,w,h) = cv2.boundingRect(cnt);
        area = cv2.contourArea(cnt);
        if(area>int(3000)):
            centro = center(x,y,w,h);
            cv2.putText(frame,str(i),(x+5,y+15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,255),2);
            cv2.circle(frame,centro,4,(0,0,255),-1);
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2);
            if(len(detects) <= i):
                detects.append([]);

            detects[i].append(centro)




            i+=1;

    if(len(contours)==0):
        detects.clear();

    else:
        for detect in detects:
            for (c,l) in enumerate(detect):

                if detect[c-1][1] < post and l[1] > post :
                    detect.clear()
                    up+=1
                    total+=1
                    cv2.line(frame,xy1,xy2,(0,255,0),5)
                    continue

                if detect[c-1][1] > post and l[1] < post:
                    detect.clear()
                    down+=1
                    total+=1
                    cv2.line(frame,xy1,xy2,(0,0,255),5)
                    continue

                #if(c>0):
                    #cv2.line(frame,detect[c-1],l,(0,0,255),1);




    cv2.putText(frame,"TOTAL:"+str(total),(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,255),2);
    cv2.putText(frame,"SUBINDO:"+str(up),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2);
    cv2.putText(frame,"DESCENDO:"+str(down),(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2);

    cv2.imshow("frame",frame);
    cv2.imshow("gray",gray);
    cv2.imshow("fgmask",fgmask);

    cv2.imshow("closing",closing);






    if cv2.waitKey(38) & 0XFF == ord("q"):
        break


cap.release();

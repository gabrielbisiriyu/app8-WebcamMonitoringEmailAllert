import cv2
import time
from emailing import  send_email
import os,shutil
from glob import glob 
from threading import Thread
video=cv2.VideoCapture(0)  
time.sleep(1) 
first_frame=None
status_list=[] 
count=1

def clean_folder():
    print("Cleaning started...")
    # To make the function wait so that the email function can quickly execute
    time.sleep(0.1) 
    # List of the image files to be deleted
    images=glob("images/*.png") 
    for image in images:
        
        os.remove(image)
    print("Cleaning ended")
while True: 
    status=0
    check,frame=video.read()
    
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) 
    gray_frame_gau=cv2.GaussianBlur(gray_frame,(21,21),0) 
     
    if first_frame is None:
        first_frame=gray_frame_gau 
    delta_frame=cv2.absdiff(first_frame,gray_frame_gau)   
    thresh_frame=cv2.threshold(delta_frame,60,255,cv2.THRESH_BINARY)[1]  
    dil_frame=cv2.dilate(thresh_frame,None,iterations=2)
    
    contours,check=cv2.findContours(dil_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
    for contour in contours:
        if cv2.contourArea(contour) <6800: 
            continue 
        x,y,w,h=cv2.boundingRect(contour)  
        rectangle=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3) 
        if rectangle.any():
            status=1
            cv2.imwrite(f"images/{count}.png",frame) 
            count=count+1
            all_images=glob("images/*.png")   
            index=int(len(all_images)/2)
            chosen_image=all_images[index]  
     
    status_list.append(status)  
    status_list=status_list[-2:] 

    if status_list[0]==1 and status_list[1]==0:
        # Threading makes the email function to run silently
        # And concurrently with the main scripts
        # This was done to prevent lagging
        email_thread=Thread(target=send_email,args=(chosen_image, ))  
        email_thread.daemon=True 
        


        email_thread.start()
    
        clean_folder()

        
    cv2.imshow("myvideo",frame)    
    
    key=cv2.waitKey(1) 
    if key == ord("q"):
        break
video.release() 

clean_folder() 


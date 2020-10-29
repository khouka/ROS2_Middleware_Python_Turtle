import cv2
import numpy as np
import imutils
import time

while True:
   img = cv2.imread("images/red.jpg") # Defining our image
   hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #Convert the image in the BGR color space to the HSV color space.
   low_red = np.array([160, 155, 84]) # Define the upper bound of the red color in hsv format 
   high_red = np.array([180, 255, 255]) # Define the lower bound of the red color in hsv format 
   red_mask = cv2.inRange(hsv, low_red, high_red) # Returns a mask, specifies which pixels fall into the upper and lower bound range.
   red_img = cv2.bitwise_and(img, img, mask = red_mask) # Applying the mask to the image
   cv2.imshow("Original Image", img) # Name of the window and the image to be shown  
   cv2.imshow("Red Detection", red_img) # Display another window for the mask 
   key = cv2.waitKey(1) #Set the delay to 1 ms
   if key == 27: # Press esc key to exit 
     break   
   cnts_red = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Finding the Contours for the red mask 
   cnts_red = imutils.grab_contours(cnts_red)
   for r in cnts_red:
      if cv2.contourArea(r) > 1000: # If detected execute the following
         print('Red was detected')
         time.sleep(1.5) # Suspends execution for 1.5 seconds  





from skimage.feature import hog
import joblib
from skimage import color
from imutils.object_detection import non_max_suppression
from skimage.transform import pyramid_gaussian
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
from Etiquetado_HOG import *
#Define HOG Parameters
# change them if necessary to orientations = 8, pixels per cell = (16,16), cells per block to (1,1) for weaker HOG
orientations = 9
pixels_per_cell = (8, 8)
cells_per_block = (2, 2)
threshold = .3

# define the sliding window:
def sliding_window(image, stepSize, windowSize):# image is the input, step size is the no.of pixels needed to skip and windowSize is the size of the actual window
    # slide a window across the image
    for y in range(0, image.shape[0], stepSize):# this line and the line below actually defines the sliding part and loops over the x and y coordinates
        for x in range(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[y: y + windowSize[1], x:x + windowSize[0]])
#%%
# Upload the saved svm model:
model = joblib.load("C:/Users/usuario/Documents/MATLAB/Scripts_Aragon/model_name.npy")

path_waterfalls= "C:/Users/usuario/Desktop/TESTMINIDAS/"
files_bbdd = os.listdir(path_waterfalls)

for j in files_bbdd:
    # Test the trained classifier on an image below!
    scale = 0
    detections = []
    # read the image you want to detect the object in:
    img= cv2.imread(path_waterfalls+"/"+j)

    # Try it with image resized if the image is too big
    #img= cv2.resize(img,(1200,350)) # can change the size to default by commenting this code out our put in a random number

    # defining the size of the sliding window (has to be, same as the size of the image in the training data)
    (winW, winH)= (64,32)
    #(winW, winH)= (64,128)
    
    windowSize=(winW,winH)
    downscale=1.5
    stepSize=16
    # Apply sliding window:

    #for resized in pyramid_gaussian(img, downscale=1.5):
        # loop over the sliding window for each layer of the pyramid
    for (x,y,window) in sliding_window(img, stepSize, windowSize):
        # if the window does not meet our desired window size, ignore it!
        if window.shape[0] != winH or window.shape[1] !=winW: # ensure the sliding window has met the minimum size requirement
            continue
        window=color.rgb2gray(window)
        fds = hog(window, orientations, pixels_per_cell, cells_per_block, block_norm='L2')  # extract HOG features from the window captured
        fds = fds.reshape(1, -1) # re shape the image to make a silouhette of hog
        pred = model.predict(fds) # use the SVM model to make a prediction on the HOG features extracted from the window
        
        if pred == 1:
            if model.decision_function(fds) > 1.5:  # set a threshold value for the SVM prediction i.e. only firm the predictions above probability of 0.6
                #print("Detection:: Location -> ({}, {})".format(x, y))
                #print("Scale ->  {} | Confidence Score {} \n".format(scale,model.decision_function(fds)))
                detections.append((int(x * (downscale**scale)), int(y * (downscale**scale)), model.decision_function(fds),
                                    int(windowSize[0]*(downscale**scale)), # create a list of all the predictions found
                                        int(windowSize[1]*(downscale**scale))))
    scale+=1
        
        

    clone = img.copy()
    #for (x_tl, y_tl, _, w, h) in detections:
        #cv2.rectangle(img, (x_tl, y_tl), (x_tl + w, y_tl + h), (0, 255, 0), thickness = 2)
        #f = open("C:/Users/usuario/Documents/MATLAB/Scripts_Aragon/Energy_Maps/BBDD/"+j+".txt",'a')
        #f.write(str(x_tl)+"\n"+str(y_tl)+"\n"+str(x_tl+w)+"\n"+str(y_tl+h)+"\n")
        #f.write("\n")
        #f.close()
    rects = np.array([[x, y, x + w, y + h] for (x, y, _, w, h) in detections]) # do nms on the detected bounding boxes
    sc = [score[0] for (x, y, score, w, h) in detections]
    #print("detection confidence score: ", sc)
    sc = np.array(sc)
    pick = non_max_suppression(rects, probs = sc, overlapThresh = 0.1)
    #print(len(pick))
    points=[]    
    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(img, (xA, yA), (xB, yB), (255,0,0), 2)
        points.append([xA,yA,xB,yB])
        #print((str(xA)+"\n"+str(yA)+"\n"+str(xB)+"\n"+str(yB)+"\n"))
    cv2.imshow("Raw Detections after NMS", img)
    print(points)
    extract_pattern(points,j)

    #### Save the images below
    k = cv2.waitKey(0) & 0xFF 
    if k == 27:             #wait for ESC key to exit
        cv2.destroyAllWindows()
    elif k == ord('s'):
        cv2.imwrite('Path\to_the_directory\of_saved_image.png',img)
        cv2.destroyAllWindows()
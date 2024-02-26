import cv2
import numpy as np
from matplotlib import pyplot as plt
#from osgeo import gdal
import subprocess
import os

max_w=0
max_h=0
''''
def maxwh(a,b):
    if a>max_w:
        max_w=a
    if b>max_h:
        max_h=b
'''
def connected(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    ##this is thinning
    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)
    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_LABEL_PIXEL,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    thresh = cv2.subtract(sure_bg,sure_fg)
    return thresh
  


def make_canvas_file(list1,width,height,t):
    cf_w=0
    cf_h=0
    space=5
    a=0
    
    for i in list1:             #finding max no of characters 
        for j in i:             #
            if len(j)>a:        #
                a=len(j)    
    cf_w=(width+space)*a
    cf_h=(height+space)*a
    
    big_img=np.zeros((cf_w,cf_h,3),t)
    for i in range(len(list1)):
        a=list1[i]
        for j in range(len(a)):
            #_,_,x,y,w,h=a[j]
            index_x=i*width
            index_y=j*height
            roi=list1[i][j]
            big_image[index_x:index_x+width,index_y:index_y+height]=roi  
    cv2.imshow("canvas file",big_image)        
    

fn='C:\Users\HP\Desktop\given\TIFF_IMAGES_AND_BOX_PAIRS\eng3.hsf.exp0.png'
'''
try:
     img=cv2.imread(fn)
     if img==None:
         print "img is empty"
except:
    print "type the correct format"
'''
img=cv2.imread(fn)
img1=img
thresh=connected(img)

#cv2.namedWindow("thresh")
#cv2.imshow("thresh",thresh)

#plt.subplot(121),plt.imshow(img,cmap='gray')
#plt.title('img'), plt.xticks([]), plt.yticks([])

img,contours,hierarchy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
max_w=0
max_h=0
list1=[[]]
list1=[[None]]*37
for i in range(len(contours)):
    if hierarchy[0,i,3]==-1:
        cnt=contours[i]
        x,y,w,h = cv2.boundingRect(cnt)
        img1 = cv2.rectangle(img1,(x,y),(x+w,y+h),(0,255,0),1)
        cv2.namedWindow('contour',cv2.WINDOW_AUTOSIZE)
        cv2.imshow("contour",img1)
        cv2.waitKey(1000)
        src=img1[x:x+w,y:y+h]
        print "Enter the key as can be seen in the image,if irrelevant press escape key"
        img1 = cv2.rectangle(img1,(x,y),(x+w,y+h),(0,0,255),1)
        sub=img1[x:x+w,y:y+h]
        command = raw_input("Please make a selection: ")
        proc=subprocess.Popen([command],shell=True,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        proc.wait()
        _,key1=proc.communicate()

        if w>max_w:
            max_w=w
        if h>max_h:
            max_h=h
        
        key=key1[1]
        #l=(fn,key,x,y,w,h)
        k=ord(key)
        #print k
        if k>=65 | k<91:
            r=k-65
        if k>=97 | k<123:
            r=k-97
        if k>=48 | k<58:
            r=k-48+26
        if k==27:
            r=37
        #print r
        if list1[r] != None:
            list1[r].append(sub)
        else:
            list1[r]=sub

        
make_canvas_file(list1,max_w,max_h,img.dtype)        


cv2.namedWindow('contours')
cv2.imshow('contours',img1)
print len(contours)

if cv2.waitKey()==ord('q'):
    cv2.destroyAllWindows()


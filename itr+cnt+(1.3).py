import cv2.cv as cv
import cv2
import tesseract
import numpy as np
import glob
import os
import subprocess
from matplotlib import pyplot as plt
import threading
global symbol
global conf
symbol=[0]
conf=[0]
a=dict()
a[0]="hsf00"
a[1]="hsf01"
a[2]="hsf02"
a[3]="hsf03"

a[4]="hsf10"
a[5]="hsf11"
a[6]="hsf12"
a[7]="hsf13"
a[8]="hsf20"
a[9]="hsf21"
a[10]="hsf22"

a[11]="hsf23"
a[12]="hsf24"

a[13]="hsf04"
a[14]="hsf30"
a[15]="hsf31"
a[16]="hsf32"
a[17]="hsf33"
a[18]="hsf34"
a[19]="hsf35"

a[20]="hsf40"
a[21]="hsf41"
a[22]="hsf43"
a[23]="hsf50"
a[23]="hsf51"
a[23]="hsf52"
a[23]="hsf53"
a[23]="hsf54"

a[24]="hsf60"
a[25]="hsf61"
a[26]="hsf62"
a[27]="hsf63"
a[28]="hsf64"
a[29]="hsf65"
a[30]="hsf66"
a[31]="hsf6extra"
a[32]="hsf6nuts"

a[33]="hsf70"
a[34]="hsf71"

a[35]="hsf72"
a[36]="hsf73"
a[37]="hsf74"
#a[38]="hsf80"

#a[39]="hsf82"
#a[40]="hsf81"
#a[41]="hsf84"
#a[42]="hsf85"
#a[43]="hsf86"
a[44]="hsf90"
a[45]="hsf91"
a[46]="hsf92"
a[47]="hsf93"
a[48]="hsf94"
a[49]="hsf95"
a[50]="hsf55"
#a[51]="hsf8nuts"
a[51]="hsf8"


def tesseract_testing(sub,i):
    for i in a.keys():
        api=tesseract.TessBaseAPI()
        BLACK=[0,0,0]
        
        image = cv.CreateImageHeader((sub.shape[1], sub.shape[0]), cv.IPL_DEPTH_8U, 1)
        cv.SetData(image, sub.tostring(), sub.dtype.itemsize * 1 * sub.shape[1])########size of the image buffer, but the image step. The step is the number of bytes i
                                                                    #n one row of your image, which is pixel_depth * number_of_channels * image_width. The pixel_depth parameter is the size in by[l]tes of the data associated to one channel. In your example,
        #print image                                                                      #   it would be simply the image width (only one channel, one byte per pixel)
        row=image.width
        col=image.height
        #part3=image[2*row/3:row,2*col/3:col]
        cv.ShowImage("image", image)
        cv2.waitKey(20)
        
        api.Init(".",a[i],tesseract.OEM_DEFAULT)
        api.SetPageSegMode(tesseract.PSM_SINGLE_CHAR)
        tesseract.SetCvImage(image,api)
        api.Recognize(None)
        level=tesseract.RIL_SYMBOL ###Block -> Para -> TextLine -> Word -> Symbol
        ri=api.GetIterator()
        if ri != None:
            s=ri.GetUTF8Text(0)
            t=ri.Confidence(0)
        api.End()
        #print conf
        conf.append(t)
        symbol.append(s)
    indx=conf.index(max(conf))
    return indx


####eng8all+eng86g+eng82z+eng8tvy+eng81+eng8ceg+eng8qd0+eng8b+eng8a

'''
api_sh.SetVariable("applybox_learn_chars_and_char_frags_mode","1")
api_sh.SetVariable("tessedit_adapt_to_char_fragments",'1')
api_dhruv.SetVariable("applybox_learn_chars_and_char_frags_mode","1")
api_dhruv.SetVariable("tessedit_adapt_to_char_fragments",'1')
api_sh.SetVariable("load_system_dawg",'F')
api_sh.SetVariable("load_freq_dawg",'F')
api_sh.SetVariable("load_punc_dawg",'F')
api_sh.SetVariable("load_number_dawg",'F')
api_sh.SetVariable("load_unambig_dawg",'F')
api_sh.SetVariable("load_bigram_dawg",'F')
api_sh.SetVariable("load_fixed_length_dawgs",'F')
'''
sub=np.zeros((60,30,1),np.uint8)

#path="C:/Users/HP/Desktop/font classification/00010/"
path= "C:/Jkd/Data/Cam3 April 6 2016 1700/ROI/result/NONSTANDARD/plate_ext/test2"
#print 2
files=glob.glob(os.path.join(path,"*.jpg"))
count=0
file1=open('outputs.txt','w')

for f in files:
    file1.write(str(f)+'\n')
    print f
    count=count+1
    #print count
    #image=cv.LoadImage(f, cv.CV_LOAD_IMAGE_GRAYSCALE)
    img=cv2.imread(f)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, inv = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    kernel=np.ones((3,3),np.uint8)
    #k=cv2.erode(inv,kernel,2)
    inv1=inv.copy()
    kernel1=cv2.getStructuringElement(cv2.MORPH_RECT,(80,10))
    l=cv2.dilate(inv1,kernel1,20)
    contours,hierarchy=cv2.findContours(l,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    temp=len(contours)
    parts=[[0]]*10
    #print temp
    x=[0]*50
        
    y=[0]*50
    w=[0]*50
    h=[0]*50

    for i in range(temp):
        
        parts[i]=np.zeros((inv.shape[0],inv.shape[1]),np.uint8)
        x[i],y[i],w[i],h[i]=cv2.boundingRect(contours[i])
        t=inv1[y[i]:y[i]+h[i],x[i]:x[i]+w[i]].copy()
        parts[i][y[i]:y[i]+h[i],x[i]:x[i]+w[i]]=t
        
    
    
    #s=sorted(range(i), key=lambda indx: y[indx])
    #print s
    symbol=[0]*100
    conf=[0]*100
    for j in range(temp):    
        #print parts[0]
        copy=parts[j].copy()

        contour,hierarchy=cv2.findContours(parts[j],cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        k=0
        for k in range(0,len(contour)):
            if hierarchy[0,k,3]==-1 :
                cnt=contour[k]
                x[k],y[k],w[k],h[k] = cv2.boundingRect(cnt)
                
        s=sorted(range(k), key=lambda indx: x[indx])
        
        for l in s:
            #print l
            if h[l]>10 and w[l]>5:
                cv2.rectangle(img,(x[l],y[l]),(x[l]+w[l],y[l]+h[l]),(255,255,255),1)
                cv2.imshow('name.jpg',img)
                cv2.waitKey(50)
                
                t=copy
                sub=255*np.zeros((h[l],w[l]),np.uint8)
                new=t[y[l]:y[l]+h[l],x[l]:x[l]+w[l]]
                sub=new
                
                _,sub=cv2.threshold(sub,127,255,cv2.THRESH_BINARY)
                sub=cv2.copyMakeBorder(sub,30,30,30,30,cv2.BORDER_CONSTANT,value=[0,0,0])
                new=cv2.copyMakeBorder(new,30,30,30,30,cv2.BORDER_CONSTANT,value=[0,0,0])
                c,hrchy=cv2.findContours(sub,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
                t=[0]*50
                for i in range(len(c)):
                    t[i]=c[i].size
                indx=t.index(max(t))
                cv2.drawContours(sub,c,indx,(255,255,255),-1)
                sub=cv2.bitwise_and(sub,new)
                
                #cv2.imshow('name.jpg',new)
                #cv2.waitKey(50)
                #print i
                #sub=new
            
                indx=tesseract_testing(sub,i)
                    
                if conf[indx]<=60 or conf[indx]==None or w[l]>1.5*np.mean(w):
                    kernel1=cv2.getStructuringElement(cv2.MORPH_CROSS,(5,6))
                    sub=cv2.erode(sub,kernel1,10)
                    #sub=cv2.morphologyEx(sub,cv2.MORPH_OPEN,kernel1, iterations = 1)
                    indx=tesseract_testing(sub,i)
                    
                    
                print symbol[indx],conf[indx]
                file1.write(str(symbol).rstrip('\n')+' ')
            del symbol[:]
            del conf[:]
                    
            '''

            command = raw_input("enter for next")
            proc=subprocess.Popen([command],shell=True,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            _,key=proc.communicate()
            proc.wait()

            ''' 
                
                    
        
    file1.write('\n')
cv2.destroyAllWindows()
#proc.kill()
file1.close()

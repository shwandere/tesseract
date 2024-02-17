import cv2.cv as cv
import cv2
import tesseract
import numpy as np
import glob
import os
import subprocess
from matplotlib import pyplot as plt



def goto(f):
    image=cv.LoadImage(f, cv.CV_LOAD_IMAGE_GRAYSCALE)
    tesseract.SetCvImage(image,api_sh)
    api_sh.Recognize(None)
    api_dhruv.Recognize(None)
    ri1=api_sh.GetIterator()
    ri2=api_dhruv.GetIterator()
    level=tesseract.RIL_SYMBOL ###Block -> Para -> TextLine -> Word -> Symbol
    print level
    #print ri.Next(level)
    t=[]
    symbol=[]
    if (ri!=0):
        #print 'e'
        symbol['ri1']=ri1.GetUTF8Text(level)
        symbol2['ri2']=ri2.GetUTF8Text(level)
        #print symbol1
        t['ri1']=ri1.Confidence(level)
        t['ri2']=ri2.Confidence(level)
        s=t.index(max(t))
        print symbol[s]
        print max(t)
        #print ri.Confidence(level)
        '''
        if symbol != None:
            f1.write(symbol+str(ri.Confidence(level)))
        
        if symbol != None:
            ci=tesseract.ChoiceIterator(ri)
            #print 'f'
            while ci.Next():
                word=ci.GetUTF8Text()
                conf=ci.Confidence()
                print word,conf
                f1.write(word+str(conf))
        f1.write('/n ')
        return symbol
        '''
api_dhruv =tesseract.TessBaseAPI()
api_dhruv.Init(".","hsf00+hsf01+hsf02+hsf03+hsf04+hsf10+hsf11+hsf12+hsf13+hsf20+hsf21+hsf22+hsf23+hsf24+hsf30+hsf31+hsf32+hsf33+hsf34+hsf35+hsf40+hsf41+hsf43+hsf50+hsf51+hsf52+hsf53+hsf54+hsf55+hsf60+hsf61+hsf62+hsf63+hsf64+hsf65+hsf66+hsf70+hsf71+hsf72+hsf73+hsf74+hsf75+hsf90+hsf91+hsf92+hsf93+hsf94+hsf95+hsf86+hsf84+hsf82+hsf85",tesseract.OEM_DEFAULT)
#f1=open("C:/Jkd/Data/CAM1_15APR/plate_ext/8",'w')
api_sh=tesseract.TessBaseAPI()

####eng8all+eng86g+eng82z+eng8tvy+eng81+eng8ceg+eng8qd0+eng8b+eng8a

api_sh.Init(".","hsf0to90+hsf0to91+hsf0to92+hsf0to93+hsf0to94+hsf0to95+hsf0to96",tesseract.OEM_DEFAULT)
api_dhruv.SetPageSegMode(tesseract.PSM_SINGLE_CHAR)
api_sh.SetPageSegMode(tesseract.PSM_SINGLE_CHAR)

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
path="C:/Python27/anpr/test"
#print 2
files=glob.glob(os.path.join(path,"*.png"))
count=0
for f in files:
    count=count+1
    print count
    #image=cv.LoadImage(f, cv.CV_LOAD_IMAGE_GRAYSCALE)
    i=cv2.imread(f)
    
    gray = cv2.cvtColor(i,cv2.COLOR_BGR2GRAY)
    ret, inv = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    kernel=np.ones((3,3),np.uint8)
    k=cv2.erode(inv,kernel,2)
    inv1=inv

    contour,hierarchy=cv2.findContours(inv,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    cv2.imshow('inv',i)
    for j in range(len(contour)):
        if hierarchy[0,j,3]==-1 :
            cnt=contour[j]
            x,y,w,h = cv2.boundingRect(cnt)
            img1 = cv2.rectangle(i,(x,y),(x+w,y+h),(0,255,0),1)
            if h>20 and w>10:
                new=k[y:y+h,x:x+w]
                sub=255*np.zeros((h,w,3),np.uint8)
                sub=new
                cv2.drawContours(sub,contour,j,(255,255,255),cv.CV_FILLED, 8, hierarchy)
                #sub=cv2.bitwise_and(new,sub)
                cv2.imshow('name.jpg',sub)
                cv2.waitKey(50)
                #print i
                #sub=new
                image = cv.CreateImageHeader((sub.shape[1], sub.shape[0]), cv.IPL_DEPTH_8U, 1)
                cv.SetData(image, sub.tostring(), sub.dtype.itemsize * 1 * sub.shape[1])########size of the image buffer, but the image step. The step is the number of bytes i
                                                                                                        #n one row of your image, which is pixel_depth * number_of_channels * image_width. The pixel_depth parameter is the size in bytes of the data associated to one channel. In your example,
                print image                                                                      #   it would be simply the image width (only one channel, one byte per pixel)
                row=image.width
                col=image.height
                #part3=image[2*row/3:row,2*col/3:col]
                cv.ShowImage("image", image)
                
                #cv2.imshow("image",sub)
                cv2.waitKey(20)
                #plt.imshow(i,cmap='gray')
                #plt.title('img'), plt.xticks([]), plt.yticks([])
                
                print f
                #tesseract.SetCvImage(image,api_dhruv)
                #text1=api_dhruv.GetUTF8Text()
                #conf1=api_dhruv.MeanTextConf()
                #print "dh "
                #print conf1,text1
                tesseract.SetCvImage(image,api_sh)
                tesseract.SetCvImage(image,api_dhruv)
                api_sh.Recognize(None)
                api_dhruv.Recognize(None)
                ri1=api_sh.GetIterator()
                ri2=api_dhruv.GetIterator()
                level=tesseract.RIL_SYMBOL ###Block -> Para -> TextLine -> Word -> Symbol
                print level
                #print ri.Next(level)
                t=[0]*2
                symbol=[0]*2
            
                if (ri1!=None) and (ri2!=None):
                    #print 'e'
                    symbol[0]=ri1.GetUTF8Text(0)
                    symbol[1]=ri2.GetUTF8Text(0)
                    t[0]=ri1.Confidence(level)
                    t[1]=ri2.Confidence(level)
                    s=t.index(max(t))
                    print symbol[s],max(t)
                    #print ri.Confidence(level)
                    #symbol1=ri.GetHocrText(level)
                    #print symbol1
                print symbol[0],t[0]
                '''
                
                else:
                
                    if symbol[0] !=None:
                        print symbol[0],ri1.Confidence(0)
                    if symbol[1] !=None:
                        print symbol[1],ri2.Confidence(0)
                    
                    if symbol != None:
                        f1.write(symbol+str(ri.Confidence(level)))
                    if symbol != None:
                        ci=tesseract.ChoiceIterator(ri)
                        #print 'f'
                        while ci.Next():
                            word=ci.GetUTF8Text()
                            conf=ci.Confidence()
                            print word,conf
                            f1.write(word+str(conf))
                    f1.write('/n ')
                    '''
                    
                '''
                if symbol=='C':
                
                    name=str(s)+'.jpg'
                    cv2.imwrite(name,i)
                
                j=0
                while symbol==None and j!=2:
                    kernel1=cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
                    i=cv2.erode(i,kernel1,iterations=1)
                    #ret,j=cv2.threshold(i,127,255,cv2.THRESH_BINARY)
                    cv2.imwrite(f,i)
                    symbol=goto(f)
                    j=j+1
                '''
                #text2=api_sh.GetUTF8Text()
                #conf2=api_sh.MeanTextConf()
                #print "sh"
                #print conf2,text2
                
                #plt.show()
               
                command = raw_input("enter for next")
                proc=subprocess.Popen([command],shell=True,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                _,key=proc.communicate()
                proc.wait()
               
            image=np.zeros((h,w),np.uint8)
cv2.destroyAllWindows()
#proc.kill()

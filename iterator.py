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
    ri=api_sh.GetIterator()
    level=tesseract.RIL_SYMBOL ###Block -> Para -> TextLine -> Word -> Symbol
    print level
    #print ri.Next(level)
    if (ri!=0):
        #print 'e'
        symbol=ri.GetUTF8Text(level)
        #symbol1=ri.GetHocrText(level)
        #print symbol1
        print symbol
        print ri.Confidence(level)
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

#api_dhruv = tesseract.TessBaseAPI()
#api_dhruv.Init(".","eng5(1)",tesseract.OEM_DEFAULT)
f1=open("C:/Users/R&D/Desktop/standard data/output.txt",'w')
api_sh=tesseract.TessBaseAPI()
###eng0+eng1+eng2+eng3+eng4+eng5+eng6+eng7+eng8+eng9+engA+engB+engC+engD+engE+engF+engG+engH+engJ+engK+engL+engM+engN+engP+engQ+engR+engS+engT+engU+engV+engW+eng0X+engY+engZ+
####eng8all+eng86g+eng82z+eng8tvy+eng81+eng8ceg+eng8qd0+eng8b+eng8a
###eng123++hsfb0+hsfb1+hsfb2+hsfl0+hsfl+hsfl2+hsfr0+hsfr1+hsfr2+hsfu0+hsfu1+hsfu2
###hsfb0+hsfb2+hsfd0+hsfd1+hsfd2
api_sh.Init(".","hsf01+hsf02+hsf03+hsf60+hsf61+hsf62+hsf63+hsf64+hsf65+hsf66",tesseract.OEM_DEFAULT)
#api_dhruv.SetPageSegMode(tesseract.PSM_SINGLE_CHAR)
api_sh.SetPageSegMode(tesseract.PSM_SINGLE_CHAR)


api_sh.SetVariable("applybox_learn_chars_and_char_0rags_mode","1")
api_sh.SetVariable("load_system_dawg",'F')
api_sh.SetVariable("load_freq_dawg",'F')
api_sh.SetVariable("load_punc_dawg",'F')
api_sh.SetVariable("load_number_dawg",'F')
api_sh.SetVariable("load_unambig_dawg",'F')
api_sh.SetVariable("load_bigram_dawg",'F')
api_sh.SetVariable("load_fixed_length_dawgs",'F')
s=0

path="F:/Wrongly read/new"
#print 2
files=glob.glob(os.path.join(path,"*.jpg"))
for f in files:
    #print 1
    image=cv.LoadImage(f, cv.CV_LOAD_IMAGE_GRAYSCALE)
    i=cv2.imread(f)

    #print i
    row=image.width
    col=image.height
    #part3=image[2*row/3:row,2*col/3:col]
    cv2.imshow("image",i)
    
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
    api_sh.Recognize(None)
    ri=api_sh.GetIterator()
    level=tesseract.RIL_SYMBOL ###Block -> Para -> TextLine -> Word -> Symbol
    print level
    #print ri.Next(level)
    if (ri!=0):
        #print 'e'
        symbol=ri.GetUTF8Text(level)
        #symbol1=ri.GetHocrText(level)
        #print symbol1
        print symbol
        print ri.Confidence(level)
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
        dst='C:/Users/R&D/Desktop/need_erosion/'+str(s)+'.jpg'
        if symbol=='None':
            shutil.move(src,dst)
            s=s+1
        q=cv2.waitKey(0)
        if q==ord('q'):
            shutil.move(src,dst)
            s=s+1
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
    '''
    command = raw_input("enter for next")
    
    proc=subprocess.Popen([command],shell=True,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    _,key=proc.communicate()
    proc.wait()
    '''
cv2.destroyAllWindows()
#proc.kill()

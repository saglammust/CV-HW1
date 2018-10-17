import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys

if len(sys.argv) == 3:
    imIn = cv2.imread(str(sys.argv[1]))
    imTo = cv2.imread(str(sys.argv[2]))
else:
    print("usage: python try0v1.py 'input_image' 'sample_image'\n"
    "Please enter the pathways of the images correctly")

def create_hist(I):
    R,C,B = I.shape
    hist = np.zeros([256,1,B])
    for r in range(R):
        for c in range(C):
            for b in range(B):
                hist[I[r,c,b],0,b] += 1
    return hist

def pdf_create(hist):
    pdf = np.zeros([256,1,3])
    for i in range(3):
        pdf[...,i] = hist[...,i]/np.sum(hist[...,i])
    return pdf

def cdf_create(pdf):
    cdf = np.zeros([256,1,3])
    for b in range(3):
        cdf[0,0,b] = pdf[0,0,b]
        for i in range(1,256):
            cdf[i,0,b] = cdf[i-1,0,b] + pdf[i,0,b]
    return cdf

def generate_LUT(cdfIn, cdfTo):
    LUT = np.zeros((256,1,3), dtype = np.uint8)
    for b in range(3):
        gTo = 0
        for gIn in range(256):
            while gTo < 256 and cdfTo[gTo,0,b] < cdfIn[gIn,0,b]:
                gTo = gTo + 1
            LUT[gIn,0,b] = gTo
    return LUT

def remapper(I,LUT):
    R, C, B = I.shape
    K = np.zeros((R,C,B), np.uint8) #create blank image
    for b in range(B):              #going through every base B->G->R
        for r in range(R):          #for loops to remap pixels
            for c in range(C):
                K[r,c,b] = LUT[I[r,c,b],0,b]
    return K                        #return the new image


hist_In = create_hist(imIn)
hist_To = create_hist(imTo)

pdf_In = pdf_create(hist_In)
pdf_To = pdf_create(hist_To)

cdf_In = cdf_create(pdf_In)
cdf_To = cdf_create(pdf_To)

LUT = generate_LUT(cdf_In, cdf_To)
imFin = remapper(imIn,LUT)

cv2.imshow("Input", imIn)
cv2.imshow("Target", imTo)
cv2.imshow("Result", imFin)
"""
plt.bar(range(256), hist_In[:,0,0], color = 'b')
plt.bar(range(256), hist_In[:,0,1], color = 'g')
plt.bar(range(256), hist_In[:,0,2], color = 'r')
plt.show()
plt.bar(range(256), hist_To[:,0,0], color = 'b')
plt.bar(range(256), hist_To[:,0,1], color = 'g')
plt.bar(range(256), hist_To[:,0,2], color = 'r')
"""
plt.show()
k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()

import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys

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

#!/usr/bin/env python


from csv import reader
from os import close

import skfuzzy as fuzz
import numpy as np
import matplotlib.pyplot as plt


class memberFn():
    "A membership function data structure"

    def __init__(self, a=0, b=0, c=0, d=0) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    #def Calculate(propBlack, topProp, leftProp):



def naive_bayes_classifier(input_filepath):
    # input is the full file path to a CSV file containing a matrix representation of a black-and-white image

    with open(input_filepath, 'r') as input_file:

        allRows = []
        row_list = list(reader(input_file, delimiter='\n'))

        # parsing rows
        for row in row_list:
            row_obj = row[0].split(',')
            allRows.append(row_obj)

        imageHeight = len(row_list)  #  number of rows/pixels in image
        imageWidth = len(row_list[0][0].split(','))  # number of pixels

        row_number = 0   # tracking row number
        pixel_number = 0  # tracking pixel number
        blackTotal = 0  # the # of black pixels in the image
        blackTopTotal = 0
        blackLeftTotal = 0
        for row in allRows:  # iterate through each pixel and add up black pixels
            pixel_number = 0
            for pixel in row:

                if pixel == '1':   # check if pixel is black
                    blackTotal += 1    # add to total black pixels

                    if pixel_number <= (imageWidth/2):
                        blackLeftTotal += 1  # check if on left side of image
                    if row_number <= (imageHeight/2):
                        blackTopTotal += 1  # check if on top half of image

                pixel_number += 1
            row_number += 1

        # calculations
        totalPixels = imageWidth * imageHeight
        propBlack = float(blackTotal / totalPixels)
        topProp = float(blackTopTotal / blackTotal)
        leftProp = float(blackLeftTotal / blackTotal)

        # value check

        print()
        print('BT: ', blackTotal)
        print('BTop: ', blackTopTotal)
        print('BLeft: ', blackLeftTotal)
        ####

        print("propBlack: ", round(propBlack,2))
        print()

        

    # most_likely_class is a string indicating the most likely class, either "A", "B", "C", "D", or "E"
    # class_probabilities is a five element list indicating the probability of each class in the order [A probability, B probability, C probability, D probability, E probability]
    return most_likely_class, class_probabilities


def fuzzy_classifier(input_filepath):
    # input is the full file path to a CSV file containing a matrix representation of a black-and-white image
    with open(input_filepath, 'r') as input_file:
        row_list = list(reader(input_file, delimiter='\n'))
    

    allRows = []
    # parsing rows
    for row in row_list:
        row_obj = row[0].split(',')
        allRows.append(row_obj)
    
    imageHeight = len(row_list)  #  number of rows/pixels in image
    imageWidth = len(row_list[0][0].split(','))  # number of pixels
    row_number = 0   # tracking row number
    pixel_number = 0  # tracking pixel number
    blackTotal = 0  # the # of black pixels in the image
    blackTopTotal = 0
    blackLeftTotal = 0
    for row in allRows:  # iterate through each pixel and add up black pixels
        pixel_number = 0
        for pixel in row:
            if pixel == '1':   # check if pixel is black
                blackTotal += 1    # add to total black pixels
                if pixel_number <= (imageWidth/2):
                    blackLeftTotal += 1  # check if on left side of image
                if row_number <= (imageHeight/2):
                    blackTopTotal += 1  # check if on top half of image
            pixel_number += 1
        row_number += 1

    # calculations
    totalPixels = imageWidth * imageHeight
    propBlack = float(blackTotal / totalPixels)
    topProp = float(blackTopTotal / blackTotal)
    leftProp = float(blackLeftTotal / blackTotal)
    # value check
    print()
    print('BT: ', blackTotal)
    print('BTop: ', blackTopTotal)
    print('BLeft: ', blackLeftTotal)
    ####
    print("propBlack: ", round(propBlack,2))
    print()
    
    x = np.arange(0.,1.,0.001) # our domain from 0 to 1

    # membership functions
    mfx_pblow = fuzz.trapmf(x, (0,0,0.3,0.4))
    mfx_pbmed = fuzz.trapmf(x, (0.3,0.4,0.4,0.5))
    mfx_pbhigh = fuzz.trapmf(x, (0.4,0.5,1,1))

    mfx_tplow = fuzz.trapmf(x, (0,0,0.3,0.4))
    mfx_tpmed = fuzz.trapmf(x, (0.3,0.4,0.5,0.6))
    mfx_tphigh = fuzz.trapmf(x, (0.5,0.6,1,1))

    mfx_lplow = fuzz.trapmf(x, (0, 0, 0.3, 0.4))
    mfx_lpmed = fuzz.trapmf(x, (0.3,0.4, 0.6, 0.7))
    mfx_lphigh = fuzz.trapmf(x, (0.6,0.7,1,1))

    scaled_pb = int(propBlack * 1000)
    scaled_tp = int(topProp * 1000)
    scaled_lp = int(leftProp * 1000)

    

    print(scaled_pb,scaled_tp, scaled_lp)
    # compute rule strengths
    # using Godel t/s-norms (min/max)

    #Rule  strengths
    str_rule1 = min(mfx_pbmed[scaled_pb], max(mfx_tpmed[scaled_tp], mfx_lpmed[scaled_lp]))
    str_rule2 = min(min(mfx_pbhigh[scaled_pb], mfx_tpmed[scaled_tp]), mfx_lpmed[scaled_lp])
    str_rule3 = max(min(mfx_lplow[scaled_lp], mfx_tpmed[scaled_tp]), mfx_lphigh[scaled_lp])
    str_rule4 = min(min(mfx_pbmed[scaled_pb], mfx_tpmed[scaled_tp]), mfx_lphigh[scaled_lp])
    str_rule5 = min(min(mfx_pbhigh[scaled_pb], mfx_tpmed[scaled_tp]), mfx_lphigh[scaled_lp])

    mf_output1 = min(mfx_)
    
    
    
    

        
    # highest_membership_class is a string indicating the highest membership class, either "A", "B", "C", "D", or "E"
    # class_memberships is a four element list indicating the membership in each class in the order [A value, B value, C value, D value, E value]
    return highest_membership_class, class_memberships

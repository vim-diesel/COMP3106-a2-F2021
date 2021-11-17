#!/usr/bin/env python


from csv import reader
import numpy as np
from numpy.core.fromnumeric import argmax




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

        row_number = 1   # tracking row number
        pixel_number = 1  # tracking pixel number
        blackTotal = 0  # the # of black pixels in the image
        blackTopTotal = 0
        blackLeftTotal = 0
        for row in allRows:  # iterate through each pixel and add up black pixels
            pixel_number = 1
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

        def memby_func(x, u, o):
            return ((1 / np.sqrt(2*np.pi* pow(o,2))) * np.exp( -1/2 * pow( ((x-u)/o), 2) ))

        a_pb = memby_func(propBlack, 0.38, 0.06)
        a_tp = memby_func(topProp, 0.46, 0.12)
        a_lp = memby_func(leftProp, 0.50, 0.09)

        print(a_pb, a_tp, a_lp)
        
    print()
    print()
    print()
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
    
    imageHeight = len(row_list)  #  number of rows in image
    imageWidth = len(row_list[0][0].split(','))  # number of pixels in a row
    row_number = 1   # tracking row number
    pixel_number = 1  # tracking pixel number
    blackTotal = 0  # the # of black pixels in the image
    blackTopTotal = 0
    blackLeftTotal = 0
    for row in allRows:  # iterate through each pixel and add up black pixels
        pixel_number = 1
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

    # membership functions
    def memby_func(x,a,b,c,d):
        if x <= a:
            return 0
        elif a < x < b:
            return min((x-a)/(b-a), 1)
        elif b<=x<=c:
            return 1
        elif c < x < d:
            return max((d-x)/(d-c), 0)
        elif d <= x:
            return 0
        else:
            print("No possible return value found.")
            return -1

    pblow = memby_func(propBlack, 0, 0, 0.3, 0.4)
    pbmed = memby_func(propBlack, 0.3, 0.4, 0.4, 0.5)
    pbhigh = memby_func(propBlack, 0.4,0.5,1,1)

    tplow = memby_func(topProp, 0,0,0.3,0.4)
    tpmed = memby_func(topProp, 0.3,0.4,0.5,0.6)
    tphigh = memby_func(topProp, 0.5,0.6,1,1)

    lplow = memby_func(leftProp, 0, 0, 0.3, 0.4)
    lpmed = memby_func(leftProp, 0.3,0.4, 0.6, 0.7)
    lphigh = memby_func(leftProp, 0.6,0.7,1,1)


    #Rule  strengths
    str_rule1 = min(pbmed, max(tpmed, lpmed))
    str_rule2 = min(min(pbhigh, tpmed), lpmed)
    str_rule3 = max(min(pblow, tpmed), lphigh)
    str_rule4 = min(min(pbmed, tpmed), lphigh)
    str_rule5 = min(min(pbhigh, tpmed), lphigh)

    a = [str_rule1, str_rule2, str_rule3, str_rule4, str_rule5]

    def get_class(i):
        i+=1
        if i == 1:
            return "A"
        elif i == 2:
            return "B"
        elif i == 3:
            return "C"
        elif i==4:
            return "D"
        elif i==5:
            return "E"

    highest_membership_class = get_class(argmax(a))
    class_memberships = a

   
    # highest_membership_class is a string indicating the highest membership class, either "A", "B", "C", "D", or "E"
    # class_memberships is a four element list indicating the membership in each class in the order [A value, B value, C value, D value, E value]
    return highest_membership_class, class_memberships

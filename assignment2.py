#!/usr/bin/env python


from csv import reader
import numpy as np




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
    print('propBlack: ', propBlack)
    print('topProp: ', topProp)
    print('leftProp: ', leftProp)
    ####
    print()
    
    x = np.arange(0.,1.,0.001) # our domain from 0 to 1

    # membership functions
    def memby_func(x,a,b,c,d):
        if x <= a:
            return 0
        elif a < x < b:
            return (x-a)/(b-a)
        elif b<=x<=c:
            return 1
        elif c < x < d:
            return (d-x)/(d-c)
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



    print("PB Values: ")

    print("pblow: ", pblow)
    print("pbmed: ", pbmed)
    print("pbhigh: ", pbhigh)
    print()

    
    print("TP Values: ")
    print("tplow: ", tplow)
    print("tpmed: ", tpmed)
    print("tphigh: ", tphigh)
    print()


    print("LP Values: ")
    print("lplow: ", lplow)
    print("lpmed: ", lpmed)
    print("lphigh: ", lphigh)
    print()


    #Rule  strengths
    str_rule1 = min(pbmed, max(tpmed, lpmed))
    print("RS1: ", str_rule1)
    print("pbmed ^ (tpmed or lpmed)")

    str_rule2 = min(min(pbhigh, tpmed), lpmed)
    print("RS2: ", str_rule2)
    print("pbhigh ^ tpmed ^ lpmed ")

    str_rule3 = max(min(pblow, tpmed), lphigh)
    print("RS3: ", str_rule3)
    print("(pblow ^ tpmed) or lphigh")
    str_rule4 = min(min(pbmed, tpmed), lphigh)
    str_rule5 = min(min(pbhigh, tpmed), lphigh)


    a = [str_rule1, str_rule2, str_rule3, str_rule4, str_rule5]


    print()        
    print()        
    print()        
    # highest_membership_class is a string indicating the highest membership class, either "A", "B", "C", "D", or "E"
    # class_memberships is a four element list indicating the membership in each class in the order [A value, B value, C value, D value, E value]
    return highest_membership_class, class_memberships

import  cv2
import numpy as np
import sys

# module level variables ##########################################################################
MIN_CONTOUR_AREA = 100

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30


###################################################################################################
def main():
    imgTrainingNumbers1 = cv2.imread("Testing_Images/small.png")
    # imgTrainingNumbers1 = cv2.resize(imgTrainingNumbers1, (1516,800))


    imgGray1 = cv2.cvtColor(imgTrainingNumbers1, cv2.COLOR_BGR2GRAY)
    imgBlurred1 = cv2.GaussianBlur(imgGray1, (5, 5), 0)


    imgThresh1 = cv2.adaptiveThreshold(imgBlurred1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # cv2.imshow("imgThresh", imgThresh)  # show threshold image for reference

    imgThreshCopy1 = imgThresh1.copy()

    npaContours1, npaHierarchy1 = cv2.findContours(imgThreshCopy1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    npaFlattenedImages = np.empty((0, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))

    intClassifications = []  # declare empty classifications list, this will be our list of how we are classifying our chars from user input, we will write to file at the end

    # possible chars we are interested in are digits 0 through 9, put these in list intValidChars
    intValidChars = [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'), ord('8'), ord('9'),
                     ord('A'), ord('B'), ord('C'), ord('D'), ord('E'), ord('F'), ord('G'), ord('H'), ord('I'), ord('J'),
                     ord('K'), ord('L'), ord('M'), ord('N'), ord('O'), ord('P'), ord('Q'), ord('R'), ord('S'), ord('T'),
                     ord('U'), ord('V'), ord('W'), ord('X'), ord('Y'), ord('Z'), ord('a'), ord('b'), ord('c'), ord('d'),
                     ord('e'), ord('f'), ord('g'), ord('h'), ord('i'), ord('j'), ord('k'), ord('l'), ord('m'), ord('n'),
                     ord('o'), ord('p'), ord('q'), ord('r'), ord('s'), ord('t'), ord('u'), ord('v'), ord('w'), ord('x'),
                     ord('y'), ord('z'), ord('.'), ord(','), ord('!'), ord('?'), ord(' ')]


    for npaContour in npaContours1:
        if cv2.contourArea(npaContour) > MIN_CONTOUR_AREA:
            [intX, intY, intW, intH] = cv2.boundingRect(npaContour)

            cv2.rectangle(imgTrainingNumbers1, (intX, intY), (intX + intW, intY + intH), (0, 0, 255), 2)

            imgROI = imgThresh1[intY:intY + intH, intX:intX + intW]
            imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))

            cv2.imshow("imgROI", imgROI)
            cv2.imshow("imgROIResized", imgROIResized)
            cv2.imshow("training_numbers_small.png", imgTrainingNumbers1)

            intChar = cv2.waitKey(0)
            print(intChar)

            if intChar == 27:
                sys.exit()
            elif intChar in intValidChars:

                intClassifications.append(intChar)
                npaFlattenedImage = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
                npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)

    fltClassifications = np.array(intClassifications,
                                  np.float32)  # convert classifications list of ints to numpy array of floats
    print(fltClassifications)

    npaClassifications = fltClassifications.reshape(
        (fltClassifications.size, 1))  # flatten numpy array of floats to 1d so we can write to file later


    npa = np.loadtxt("Text_Files/dataset.txt", np.float32)
    npa1 = np.loadtxt("Text_Files/dataset_1D.txt", np.float32)
    npa = npa.reshape((npa.size, 1))

    kNearest = cv2.ml.KNearest_create()
    kNearest.train(npa1, cv2.ml.ROW_SAMPLE, npa)
    npaFlattenedImage = npaFlattenedImage.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
    npaFlattenedImage = np.float32(npaFlattenedImage)
    retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaFlattenedImage, k = 1)

    matches = npaResults == fltClassifications
    correct = np.count_nonzero(matches)
    accuracy = correct * 100.0 / npaResults.size

    print("Accuracy is = %.2f" %accuracy +"%")


    cv2.destroyAllWindows()  # remove windows from memory

    return


###################################################################################################
if __name__ == "__main__":
    main()
# end if

# print("THE\nOCEAN\nIS\nBLUE")

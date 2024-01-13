from transform import four_point_transform
from skimage.filters import threshold_local
import cv2
import imutils
import numpy as np

def pre_img(img):
    block_size = 9
    C = 5
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('img.png', img)
    #adaptiveThreshold
    th_img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, block_size, C)
    cv2.imwrite('th_img.png', th_img)
    #medianFilter
    blur = cv2.medianBlur(th_img, 3)
    cv2.imwrite('blur.png', blur)
    # 구조화 요소 커널, 사각형 (5x5) 생성 ---①
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    # 열림 연산 적용 ---②
    opening = cv2.morphologyEx(blur, cv2.MORPH_OPEN, k)
    cv2.imwrite('opening.png', opening)
    dst = cv2.cvtColor(opening,cv2.COLOR_GRAY2BGR)
    return dst

def transform_img(image):
    #image= cv2.imread('test2.jpg')
    ratio = image.shape[0]/500.0
    orig = image.copy()
    image = imutils.resize(image,height=500)

    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(5,5),0)
    edged = cv2.Canny(gray, 75, 200)
    cv2.imwrite('edge.png', edged)
    cnts = cv2.findContours(edged.copy(),cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts= sorted(cnts, key= cv2.contourArea, reverse=True)[:5]
    screenCnt = []
    for c in cnts:
        peri = cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c, 0.02*peri, True)
        if len(approx)==4:
            screenCnt = approx
            break
    if len(screenCnt)>0:
        print(screenCnt)
        #cv2.drawContours(image,[screenCnt],-1,(0,255,0),2)
        warped = four_point_transform(orig, screenCnt.reshape(4,2)*ratio)

        # warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        #T = threshold_local(warped,11,offset=10, method = "gaussian")
        #warped = (warped>T) *255
        warped_size = warped.shape[0]*warped.shape[1]
        orig_size = orig.shape[0]*orig.shape[1]
        # Check if the size of warped image is less than 1/6th of the original image size
        if warped_size*6<orig_size:
            return pre_img(image)
        else:
            return pre_img(warped)
    else:
        return pre_img(image)
    

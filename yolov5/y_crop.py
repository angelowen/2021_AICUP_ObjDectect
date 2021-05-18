import numpy as np
import cv2
import os,sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image,ImageDraw
def extract_peek_ranges_from_array(array_vals, minimun_val=500, minimun_range=20):
    print(array_vals)
    start_i = None
    end_i = None
    peek_ranges = []
    #enumerate() 函數用於將數據對象組合為一個索引序列，同時列出數據和數據下標
    for i, val in enumerate(array_vals):
        if val > minimun_val and start_i is None:
            start_i = i
        elif val > minimun_val and start_i is not None:
            pass
        elif val < minimun_val and start_i is not None:
            end_i = i
            if end_i - start_i >= minimun_range:
                peek_ranges.append((start_i, end_i))
            start_i = None
            end_i = None
        elif val < minimun_val and start_i is None:
            pass
        else:
            raise ValueError("cannot parse this case...")
    return peek_ranges

img = cv2.imread('data/images/img_1.jpg')
c_img = img[420:893,273:378]
y_up = 420
x_l = 273

gray_img = cv2.cvtColor(c_img, cv2.COLOR_BGR2GRAY)
bilateral = cv2.bilateralFilter(gray_img , 11, 75, 75)
blur = cv2.GaussianBlur(bilateral,(5,5),1) # 7,7,1
adaptive_threshold = cv2.adaptiveThreshold(
    blur,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,11, 2) # 3,2
cv2.imwrite('output_y_adap.jpg', adaptive_threshold)
# cv2.imshow('My Image', adaptive_threshold)
# cv2.waitKey(0)

vertical_sum = np.sum(adaptive_threshold, axis=0)
horizontal_sum = np.sum(adaptive_threshold, axis=1)

line_seg_adaptive_threshold = np.copy(adaptive_threshold)
peek_ranges = extract_peek_ranges_from_array(horizontal_sum)
# print("peek:",peek_ranges)
print("rect positions: ")
for i, peek_range in enumerate(peek_ranges):
    x = 0
    y = peek_range[0]
    w = line_seg_adaptive_threshold.shape[1]
    h = peek_range[1] - y
    pt1 = (x_l + x, y_up + y)
    pt2 = (x_l + x + w, y_up + y + h)
    # print(pt1 ,";", pt2,"\n")
    #cv2.rectangle(影像, 頂點座標, 對向頂點座標, 顏色, 線條寬度)
    cv2.rectangle(img, pt1, pt2, (255,0,0),4)
    print(pt1,pt2)
    #wp = pt1 + pt2
    #print(wp)
# cv2.imshow('line image',line_seg_adaptive_threshold)
cv2.imwrite('output_y_crop.jpg', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

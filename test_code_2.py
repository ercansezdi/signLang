import cv2 as cv


img_1 = cv.imread("pure_pict\\compare_images\\A\\rgb_A0.png")
img_2 = cv.imread("pure_pict\\compare_images\\B\\rgb_B0.png")

hsv_base = cv.cvtColor(img_1, cv.COLOR_BGR2HSV)
hsv_test1 = cv.cvtColor(img_2, cv.COLOR_BGR2HSV)

hist_base = cv.calcHist([hsv_base], [0, 1], None, [50, 60], [0, 180, 0, 256], accumulate=False)
cv.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
hist_test1 = cv.calcHist([hsv_test1], [0, 1], None, [50, 60], [0, 180, 0, 256], accumulate=False)
cv.normalize(hist_test1, hist_test1, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
base_base = cv.compareHist(hist_base, hist_base, 2)
base_test1 = cv.compareHist(hist_base, hist_test1, 2)
print('Base-Base = {}, Base-Test(1) = {} '.format(base_base, base_test1))
from selenium.webdriver import FirefoxOptions
import helium
import time
import pytesseract
import cv2
import numpy as np

def ratio(c, max_n, min_n):
    x,y,w,h = cv2.boundingRect(c)
    if( 1.0*w/h < max_n and 1.0*w/h > min_n):
        return True
    else:
        return False

family = "https://www.famiport.com.tw/Web_Famiport/page/process.aspx"
options = FirefoxOptions()
options.add_argument("--width=800")
options.add_argument("--height=800")
driver = helium.start_firefox(family, options=options)

helium.wait_until(helium.Text("※請輸入驗證碼。").exists)

textfields = helium.find_all(helium.TextField())
helium.write("00718624969", into=textfields[2])
helium.scroll_down(500)
driver.save_screenshot("temp.png")

img = cv2.imread("temp.png", cv2.IMREAD_GRAYSCALE)
# cv2.imwrite("gray.png", img)
ret, img = cv2.threshold(img, 175, 255, cv2.THRESH_BINARY_INV)
# cv2.imwrite("gray2.png", img)
# cv2.imshow("test", img)
# cv2.waitKey(0)
img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
(cnts, _) = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = [c for c in cnts if  cv2.contourArea(c) > 1000 and ratio(c, 4.2, 4.1)]

x, y, w, h = 0, 0, 0, 0
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(img_color, (x, y), (x + w, y + h), (36,255,12), 5)

number_area = img[y:y+h, x:x+w]
cv2.imshow("verify", number_area)
text = pytesseract.image_to_string(number_area, config="--oem 3 --psm 7 digits")
text = "".join([s for s in text if s.isdigit()])
print(text)
helium.write(text, into=textfields[7])
cv2.waitKey(0)
input()

helium.kill_browser()

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

# the id you want to check
goods_id = "00718624969"

# family url
family = "https://www.famiport.com.tw/Web_Famiport/page/process.aspx"

# init browser
options = FirefoxOptions()
options.add_argument("--width=800")
options.add_argument("--height=800")
driver = helium.start_firefox(family, options=options)

# wait until web completely loaded
helium.wait_until(helium.Text("※請輸入驗證碼。").exists)

# find all textfield
textfields = helium.find_all(helium.TextField())

# write to the fisrt goods
helium.write(goods_id, into=textfields[2])

# scroll down for viewing verification code and take screenshot
helium.scroll_down(500)
driver.save_screenshot("temp.png")

# read from screen shot as gray image
img = cv2.imread("temp.png", cv2.IMREAD_GRAYSCALE)

# convert to only black and white
ret, img = cv2.threshold(img, 175, 255, cv2.THRESH_BINARY_INV)

# for debug
img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

# find all contours
(cnts, _) = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# find verification code block ratio in all contours
cnts = [c for c in cnts if  cv2.contourArea(c) > 1000 and ratio(c, 4.2, 4.1)]

# record the position
x, y, w, h = 0, 0, 0, 0
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(img_color, (x, y), (x + w, y + h), (36,255,12), 5)

# cut out the code part
number_area = img[y:y+h, x:x+w]

# show code part image
cv2.imshow("verify", number_area)

# tesseract ocr
text = pytesseract.image_to_string(number_area, config="--oem 3 --psm 7 digits")

# extract digit from string
text = "".join([s for s in text if s.isdigit()])
print(text)

# write into the textfield
helium.write(text, into=textfields[7])
cv2.waitKey(0)

# you can do whatever you want

# wait and close the browser
input()
helium.kill_browser()

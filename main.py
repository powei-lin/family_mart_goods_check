import helium
import time
import pytesseract
import cv2
import numpy as np

family = "https://www.famiport.com.tw/Web_Famiport/page/process.aspx"
driver = helium.start_chrome(family)
helium.wait_until(helium.Text("※請輸入驗證碼。").exists)
textfields = helium.find_all(helium.TextField())
helium.write("00718624969", into=textfields[2])

helium.scroll_down(500)
driver.save_screenshot("temp.png")

# img = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
img = cv2.imread("temp.png", cv2.IMREAD_GRAYSCALE)
ret, img = cv2.threshold(img, 175, 255, cv2.THRESH_BINARY_INV)
img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
(cnts, _) = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = [c for c in cnts if cv2.contourArea(c) > 4000 and cv2.contourArea(c) < 4500]

for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(img_color, (x, y), (x + w, y + h), (36,255,12), 2)
    cv2.imshow("t", img_color)
    cv2.waitKey(0)

number_area = img[y:y+h, x:x+w]
cv2.imshow("ttt", number_area)
text = pytesseract.image_to_string(number_area, config="--oem 3 --psm 7 digits")
# text = "".join([int(s) for s in text if s.isdigit()])
text = "".join([s for s in text if s.isdigit()])
print(text)
helium.write(text, into=textfields[7])
cv2.waitKey(0)
input()

helium.kill_browser()
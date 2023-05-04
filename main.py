import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import cvzone
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)


# def drawALL(img, btnList):
#     for btn in btnList:
#         x, y = btn.pos
#         w, h = btn.size
#         cvzone.cornerRect(img, (btn.pos[0], btn.pos[1], btn.size[0], btn.size[1]),
#                           20, rt=0)
#         cv2.rectangle(img, btn.pos, (x + w, y + h), (66, 152, 245), cv2.FILLED)
#         cv2.putText(img, btn.text, (x + 15, y + 60), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)
#     return img



def drawAll(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
                      (66, 152, 245), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 40, y + 60),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0,0,0), 3)

    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out

class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

        # def draw(self,img):
        # return img


keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

finalTxt = ""

# myButton = Button([100,100],"Q")
btnList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        btnList.append(Button([100 * j + 50, 100 * i + 50], key))
# for x in range:


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)

    img = drawAll(img, btnList)

    if lmList:
        for btn in btnList:
            x, y = btn.pos
            w, h = btn.size
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, btn.pos, (x + w, y + h), (180, 60, 150), cv2.FILLED)
                cv2.putText(img, btn.text, (x + 15, y + 60), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)
                l, _, _ = detector.findDistance(8, 4, img, draw=False)
                if l < 50:
                    cv2.rectangle(img, btn.pos, (x + w, y + h), (0, 250, 0), cv2.FILLED)
                    cv2.putText(img, btn.text, (x + 15, y + 60), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)
                    finalTxt += btn.text
                    sleep(0.2)

    cv2.rectangle(img, (50, 350), (700, 450), (66, 152, 245), cv2.FILLED)
    cv2.putText(img, finalTxt, (60, 425), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

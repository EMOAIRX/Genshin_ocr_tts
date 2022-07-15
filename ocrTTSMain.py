import time
from paddleocr import PaddleOCR
import cv2
from getScreenRect import getScreenRect
from ttsRead import ttsRead
from difflib import SequenceMatcher
import pyautogui
import numpy as np

forMoreDetails = True

#image = cv2.imread("./genshin.png")
#im0 = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
#im0 = cv2.cvtColor(im0, cv2.COLOR_BGR2GRAY)

print('正在启动服务')
ttsRead('正在启动服务')

reader = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False)

def isNotASCII(s: str) -> bool:
    rate = 0
    for x in s:
        if ord(x) <= 127:
            rate += 1
    rate /= len(s)
    return rate < 4/5


lastStr = ''


def isDifferent(s: str) -> bool:
    return SequenceMatcher(None, lastStr, s).ratio() < .8


def getRegion(status: str) -> 'tuple[int, int, int, int]':
    isDetecting = (status == 'detecting')
    rect = getScreenRect()
    if isDetecting:
        return (0, 0, rect[0]*3//10, rect[1]*3//10)
    else:
        left = rect[0]//20
        right = rect[0]-left
        top = rect[1]//3
        return (left, top, right-left, rect[1]-top)


print('启动成功')
ttsRead('启动成功')
status = 'detecting'
color = {}
color['detecting'] = np.array([255, 255, 255])
color['waiting'] = np.array([238, 242, 246])
color['keeping'] = np.array([238, 242, 246])
while True:
    imPath = './youdao-ver-tmp.png'
    rect = getScreenRect()
    image = pyautogui.screenshot(region=getRegion(status))
    #获取图片，

    if forMoreDetails:
        image.save(imPath)

    im0 = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    lower_color = color[status]
    upper_color = color[status]
    im0 = cv2.inRange(im0, lower_color, upper_color)  # inrange函数将根据最小最大HSV值检测出自己想要的颜色部分
#    ret, im0 = cv2.threshold(im0, 240, 255, type=cv2.THRESH_TOZERO)
    if forMoreDetails:
        cv2.imshow("0000",im0)
        cv2.waitKey(0)
#    im0 = cv2.cvtColor(im0, cv2.COLOR_BGR2GRAY)
    im1 = cv2.resize(im0, (0, 0), fx=.5, fy=.5)

    if forMoreDetails:
        print('STARTing OCR')
    result = reader.ocr(im1)
    if forMoreDetails:
        print('End OCR')

    result = [x[1][0] for x in result]
    # x[0]是坐标信息
    # x[1]是文本和置信度信息
    result = [x for x in result if isNotASCII(x)]
    resultStr = '\n'.join(result)
    if forMoreDetails:
        print(result)

    if status == 'detecting':
        #用于判断是否存在“自动”两个字
        resultStr = '\n'.join(result)
        if resultStr.count('自动') == 0:
            print('获取到了非关键数据')
            time.sleep(0.5)
        else:
            print('检测到处于对话')
            lastStr = ''
            status = 'waiting'
    elif status == 'waiting':
        if not isDifferent(resultStr):
            print(result)
            ttsRead(resultStr)
            status = 'keeping'
        else:
            print('检测到字幕仍然在滚动')
    elif status == 'keeping':
        if isDifferent(resultStr):
            status = 'detecting'
            print('检测到画面变化，查询是否存在对话')
        else:
            print('检测到画面保持')

    lastStr = resultStr
    lastIm0 = im0
    laststatus = status

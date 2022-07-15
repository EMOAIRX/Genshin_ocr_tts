import time
from paddleocr import PaddleOCR
import cv2
from getScreenRect import getScreenRect
from ttsRead import ttsRead

import pyautogui
import numpy as np

print('正在启动服务')
ttsRead('正在启动服务')

reader = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False)


def getRegion(status: str) -> 'tuple[int, int, int, int]':
    isDetecting = (status == 'detecting')
    rect = getScreenRect()
    if isDetecting:
        return (0, 0, rect[0]*2//10, rect[1]*2//10)
    else:
        left = rect[0] * 0.17
        right = rect[0]-left
        top = rect[1]//4
        return (left, top, right-left, rect[1]-top)


print('启动成功')
ttsRead('启动成功')
status = 'detecting'
color = {}
color['detecting'] = np.array([255, 255, 255])  # 自动两个字的颜色
color['rolling'] = np.array([238, 242, 246])  # 下面文本的颜色


def get_image(status):

    image = pyautogui.screenshot(region=getRegion(status))
    # 获取图片，
    im0 = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    lower_color = color[status]
    upper_color = color[status]
    im0 = cv2.inRange(im0, lower_color, upper_color)
    # inrange函数将根据最小最大HSV值检测出自己想要的颜色部分
    return im0


def get_ocr_word(image):
    image_shrink = cv2.resize(image, (0, 0), fx=.7, fy=.7)
    result = reader.ocr(image_shrink)
    result = [x[1][0] for x in result]
    resultStr = ' '.join(result)
    return resultStr


while True:
    now_image = get_image(status)

    if status == 'detecting':
        # 用于判断是否存在“自动”两个字
        resultStr = get_ocr_word(now_image)
        print('detecting -- ', resultStr)
        if resultStr.count('自动') == 0 and resultStr.count('Auto') == 0:
            print('获取到了非关键数据')
            time.sleep(0.5)
        else:
            print('检测到处于对话')
            status = 'rolling'
            first_IMAGE = get_image(status)
            now_image = first_IMAGE
            Current_str = get_ocr_word(first_IMAGE)
            # ttsRead('第一次检测到的文本是'+Current_str)

    elif status == 'rolling':
        delta_image = now_image - pre_image

        negative = np.count_nonzero(now_image < pre_image)  # 0 - 255 = 1，负数溢出
        positive = np.count_nonzero(now_image > pre_image)

        print(positive, '-----', negative)
        print(positive)
        if negative > 5:  # 需要重新检测，估计是切屏了，或者新的一句话
            status = 'detecting'
            print('检测到画面变化，查询是否存在对话')
        elif positive < 5:  # 几乎没有变化，这个权值不知道设多少好，
            result = Current_str
            if(len(result)):
                print(result)
                ttsRead(result)
            Current_str = ''
            time.sleep(0.2)
        else:
            Current_str += get_ocr_word(delta_image)
            print('检测到字幕仍然在滚动，当前检测到文本为：', Current_str)

    pre_image = now_image

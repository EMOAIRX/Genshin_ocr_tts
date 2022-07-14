import time
from PIL import ImageGrab
import easyocr
import cv2
from getScreenRect import getScreenRect
from ttsRead import ttsRead
from difflib import SequenceMatcher

print('正在启动服务')
ttsRead('正在启动服务')

reader = easyocr.Reader(['ch_sim', 'en'])


def filter(s: str) -> bool:
    rate = 0
    for x in s:
        if ord(x) < 127:
            rate += 1
    return rate*2 < len(s)


lastStr = ''


def needRefresh(s: str) -> bool:
    return SequenceMatcher(None, lastStr, s).ratio() < .8


print('启动成功')
ttsRead('启动成功')
status = 'detecting'
while True:
    imPath = './youdao-ver-tmp.png'
    rect = getScreenRect()
    bbox = (0, 0, rect[0]*3//10, rect[1]*3//10) if status == 'detecting' else (
        rect[0]*3//20, rect[1]*2//3, rect[0]*17//20, rect[1])
    ImageGrab.grab(bbox=bbox).save(imPath)
    im0 = cv2.imread(imPath)
    im1 = cv2.resize(im0, (0, 0), fx=.5, fy=.5)
    result = reader.readtext(im1, detail=0)
    result = [x for x in result if filter(x)]
    resultStr = '\n'.join(result)
    if status == 'detecting':
        if resultStr.count('自动') == 0:
            print('获取到了非关键数据')
            time.sleep(1)
        else:
            print('检测到处于对话')
            lastStr = ''
            status = 'waiting'
    elif status == 'waiting':
        if not needRefresh(resultStr):
            print(result)
            ttsRead(resultStr)
            status = 'keeping'
        else:
            print('检测到字幕仍然在滚动')
    else:
        if needRefresh(resultStr):
            status = 'detecting'
            print('检测到画面变化，查询是否存在对话')
        else:
            print('检测到画面保持')
    lastStr = resultStr

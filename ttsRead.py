# https://dict.youdao.com/dictvoice?le=auto&audio=%E6%88%91%E6%83%8A%E4%BA%86

from urllib import parse
import requests
from myPlaysound import playsound


def fromStrToMp3(strValue: str, path: str):
    url = 'https://dict.youdao.com/dictvoice?le=auto&audio=' + \
        parse.quote(strValue, encoding='utf-8')

    r = requests.get(url)
    with open(path, 'wb') as f:
        f.write(r.content)
        f.close


max_len = 120


def ttsRead(strValue: str):
    path = './youdao-tts-tmp.mp3'
    if len(strValue) > max_len:
        strValue = strValue[:max_len:]
    fromStrToMp3(strValue, path)
    playsound(path)


if __name__ == '__main__':
    strValue = '真叫人难以置信'
    ttsRead(strValue)

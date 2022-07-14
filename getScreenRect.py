from win32 import win32api
from PIL import ImageGrab

imForScreenRect = ImageGrab.grab()
screenRect = (imForScreenRect.width,imForScreenRect.height)

def getScreenRect() -> 'tuple[int,int]':
    return screenRect


if __name__ == '__main__':
    print(getScreenRect())

from ctypes import *
import time

def loadImg(url):
    # url = "https://s3.cn-north-1.amazonaws.com.cn/lqdzj-image/YB/22/YB_22_237.jpg"
    # with urllib.request.urlopen(url) as f:
    #     data = f.read()
    # image_data = urllib.request.urlopen(url).read()

    dll = CDLL("./LayoutCutting.so")

    dll.LayoutCutting_PLZ.restype = c_char_p
    p = bytes(url, 'utf-8')  # c_wchar_p(url)
    lenth = len(url)
    print('%s %d' % (url, lenth))
    print("=========11========")
    bStr = dll.LayoutCutting_PLZ(p, lenth)
    sStr = bytes.decode(bStr)
    sStr = sStr[0:-1]
    print("=========22========")

    print(sStr)

    print(sStr.split(','))

    return sStr


if __name__ == '__main__':
        # urls = ["C:/Users/ls/Desktop/dzj/0001_001_26_01.jpg","C:/Users/ls/Desktop/dzj/0001_001_26_02.jpg","C:/Users/ls/Desktop/dzj/0001_001_26_03.jpg","C:/Users/ls/Desktop/dzj/0001_001_26_04.jpg"]
        url = "./0001_001_26_08.jpg"
        loadImg(url)

        # for urlt in urls:
        #     str = loadImg(urlt)
        #     print(str)

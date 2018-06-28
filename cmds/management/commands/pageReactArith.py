from ctypes import *
import time

def loadImg(url):
    """
    传入图片本地路径，然后使用切框算法，得出图片大框的坐标值
    :param url:图片本地路径
    :return:大框的坐标值
    """
    # url = "https://s3.cn-north-1.amazonaws.com.cn/lqdzj-image/YB/22/YB_22_237.jpg"
    # with urllib.request.urlopen(url) as f:
    #     data = f.read()
    # image_data = urllib.request.urlopen(url).read()

    dll = CDLL("./LayoutCutting.so")

    dll.LayoutCutting_PLZ.restype = c_char_p
    # p = c_wchar_p(url)
    p = c_char_p(url)
    lenth = len(url)
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
        url = b"./0001_001_26_08.jpg"
        loadImg(url)

        # for urlt in urls:
        #     str = loadImg(urlt)
        #     print(str)

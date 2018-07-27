#coding=utf-8
from ctypes import *

class StructPointer(Structure):
    _fields_ = [("final_boxes", c_char * 100), ("final_results", c_char * 100),("final_confidence", c_char * 100),("label_code", c_char * 6025),("age", c_int)]
ll = cdll.LoadLibrary
dll = ll("./libwzqg.so")
dll.txt_reco.argtypes = (c_char_p, c_char_p)
dll.txt_reco.restype = POINTER(StructPointer)
dll.multi_choice.restype = c_char_p
dll.img_segment.restype = c_char_p
dll.txt_reco.argtypes = (c_char_p, c_char_p)

def getCols(url):
    print("loadtest start!!!")
    #本地图片路径和路径字符串的长度
    # filePath = c_wchar_p(url)
    filePath = c_char_p(url)


    print("=================1")
    frame = b"140,39,223,1137"
    #frame = b"47,150,1136,674"
    colretStr = dll.img_segment(filePath, c_char_p(frame))
    colStr = bytes.decode(colretStr,"utf-8")
    print(colStr)
    colStr = colStr[0:-1]
    colStrArray = colStr.split(',')
    print(len(colStrArray))
    # for zuobiao in colStrArray:
    #     if()
    # print()
    return colStrArray

def getPieces(url):
    filePath = c_char_p(url)
    print("=================2")
    # col = b"140,39,363.00,1176.00"  # 列坐标957.00,802.00,56.00,618.00
    col = b"224,39,280,1137"  # 列坐标
    piecerelStr = dll.multi_choice(c_char_p(col), filePath)
    # pieceStr = bytes.decode(piecerelStr, "utf-8")
    pieceStr = bytes.decode(piecerelStr, "utf-8")  # label的序号文字转换表
    print(pieceStr)

    print("=================3")

    # piece = b"1034.00,197.00,1078.00,359.00"  # 单字坐标

def getPieceInfo(url):
    # piece = b"275.00,148.00,315.00,750.00"  # 单字坐标1030.00,1180.00,43.00,245.00
    piece = b"224,39,504,1176"  
    filePath = c_char_p(url)
    textStr = dll.txt_reco(c_char_p(piece), filePath)
    boxesStr = bytes.decode(textStr.contents.final_boxes)  # 检测框坐标
    resultlabel = bytes.decode(textStr.contents.final_results)  # 检测框对应的label序号
    confidencelabel = bytes.decode(textStr.contents.final_confidence)  # 识别出的label的置信度；
    textlael = bytes.decode(textStr.contents.label_code, "utf-8")  # label的序号文字转换表

    print(boxesStr)
    #boxesStr = boxesStr[0:-1]
    print("===========88")
    print(boxesStr)
    print("==============77")
    print(boxesStr.split(','))
    boxesStr = boxesStr.split(',')
    print("=================4")
    print(resultlabel)
    print("=================5")

    print(confidencelabel)
    print("=================6")

    print(textlael)
    print("=================7")

    print("load test end!!!")

    return boxesStr

    
    

if __name__ == '__main__':
        # loadtest(b"./41-V120P0192.jpg")
        getCols(b"./41.jpg")
        getPieceInfo(b"./41.jpg")
        getPieces(b"./41.jpg")

import os
from urllib.request import *

dirpath = os.makedirs('./image/', exist_ok=True)

IMAGE_URL = "http://image.nationalgeographic.com.cn/2017/1122/20171122113404332.jpg"


def download_img(url):
    """
    下载图片存储到本地，并返回路径
    :param url: 传入图片http地址
    :return: 返回本地存储图片路径
    """
    image_guid = url.split('/')[-1]
    print(image_guid)
    target = urlretrieve(url, './image/%s'% image_guid)
    return target



if __name__ == '__main__':
      img = download_img(IMAGE_URL)
      print(img[0])


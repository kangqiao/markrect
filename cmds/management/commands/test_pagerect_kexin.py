from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from tdata.models import *
from segment.models import PageRect, PageRectStatus
from cmds.management.commands.pageReactArith import loadImg
from cmds.management.commands.downImg import download_img


class Command(BaseCommand):
    def handle(self, *args, **options):
        toCutPageList = PageRect.objects.filter(status=PageRectStatus.CUT_UNCOMPLETED)
        updates = []
        for page in toCutPageList:
            img = download_img(page.img_path)  # 下载图片存储到本地，并返回路径
            zuobiaoStr = loadImg(img[0])  # 调用切框的算法，返回坐标值
            print(zuobiaoStr)  # 139,39,140,25
            print("=============11111============")
            array = zuobiaoStr.split(',')
            page.x = array[0]
            page.y = array[1]
            page.w = array[2]
            page.h = array[3]
            updates.append(page)
        PageRect.objects.bulk_update(updates)

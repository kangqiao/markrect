from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from tdata.models import *
from segment.models import PageRect, PageRectStatus
from cmds.management.commands.pageReactArith import loadImg
#from cmds.management.commands.colArith import getCols,getPieces,getPieceInfo
from cmds.management.commands.downImg import download_img


import os

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('LQSutra_sid', nargs='+', type=str)#设置一个龙泉id的参数，支持多个

    def handle(self, *args, **options):
        sids = options['LQSutra_sid']
        BASE_DIR = settings.BASE_DIR

        for sid in options['LQSutra_sid']:
            #获得对象
            try:
                lqsutra = LQSutra.objects.get(sid=sid) # 需要命令行输入
            except:
                print('龙泉经目中未查到此编号：'+sid)
                continue
            codes = ""
            if not lqsutra is None:
                sutra_list = Sutra.objects.filter(lqsutra=lqsutra)
                pagerect_list = []
                if sutra_list:
                    for sutra in sutra_list:
                        reel_list = Reel.objects.filter(sutra=sutra)
                        if reel_list:
                            for reel in reel_list:
                                print("生成{}的{}的第{}卷的标注页(PageRect)数据".format(sutra.tripitaka.name, sutra.name, reel.reel_no))
                                for page_no in range(reel.start_vol_page, reel.end_vol_page+1):
                                    if page_no < 0 :
                                        print("无法生成{}的{}的第{}卷的标注页{}(PageRect)数据".format(sutra.tripitaka.name, sutra.name, reel.reel_no, page_no))
                                        continue
                                    try:
                                        page = Page.objects.get(reel=reel, page_no=page_no)
                                    except:
                                        page = None
                                    code = reel.reel_code() + "_P" + str(page_no)
                                    codes += code +" "
                                    img_path = settings.IMAGE_URL_PREFIX + reel.url_prefix() + str(page_no)+".jpg"
                                    # img = download_img(img_path) #下载图片存储到本地，并返回路径
                                    # zuobiaoStr = loadImg(img[0])#调用切框的算法，返回坐标值
                                    # print(zuobiaoStr)#139,39,140,25
                                    # print("=============11111============")
                                    # array = zuobiaoStr.split(',')
                                    # pagerect = PageRect(code=code, img_path=img_path, page=page, x=array[0], y=array[1], w=array[2], h=array[3], status=PageRectStatus.CUT_UNCOMPLETED)
                                    pagerect = PageRect(code=code, img_path=img_path, page=page, status=PageRectStatus.CUT_UNCOMPLETED)
                                    pagerect_list.append(pagerect)
                        else:
                            print('还未导入{}的{}经的相关卷详目信息'.format(sutra.tripitaka.name, sutra.name))
                else:
                    print('还未导入龙泉经({})相关的经目信息'.format(sid))

                if pagerect_list:
                    PageRect.objects.bulk_create(pagerect_list)

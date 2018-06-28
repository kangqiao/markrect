from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from tdata.models import *
from segment.models import PageRect, PageRectStatus, ColumnRect

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
                                    try:
                                        page = Page.objects.get(reel=reel, page_no=page_no)
                                    except:
                                        page = None
                                    code = reel.reel_code() + "_P" + str(page_no)
                                    codes += code +" "
                                    img_path = settings.IMAGE_URL_PREFIX + reel.url_prefix() + str(page_no)+".jpg"
                                    # todo 下载图片, 调用可新的切列接口. 产生了xywh column_no
                                    pagerect = ColumnRect(code=code, img_path=img_path, page=page, status=PageRectStatus.CUT_COLUMN_COMPLETED)
                                    pagerect_list.append(pagerect)
                        else:
                            print('还未导入{}的{}经的相关卷详目信息'.format(sutra.tripitaka.name, sutra.name))
                else:
                    print('还未导入龙泉经({})相关的经目信息'.format(sid))

                if pagerect_list:
                    PageRect.objects.bulk_create(pagerect_list)

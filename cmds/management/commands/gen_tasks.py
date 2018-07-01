from django.core.management.base import BaseCommand, CommandError
from bulk_update.helper import bulk_update
from django.conf import settings
from tdata.models import *
from segment.models import *
from segment.gen_tasks import *
import random


class Command(BaseCommand):
    def handle(self, *args, **options):
        test_gen_pagerect_test_data()
        gen_pagerect_task()

        test_gen_column_task()
        gen_column_task()

        # Begin 测试用, 随机将部分列任务置完成状态去生成字任务数据.
        # columnTaskList = ColumnTask.objects.filter(status=TaskStatus.COMPLETED)
        # columntasks = []
        # charrects = []
        # for columnTask in columnTaskList:
        #     ColumnRect.objects.filter()
        #     if (random.randint(0, 9) / 2) == 0:
        #         for pageRect in columnTask.pagerects:
        #             columnRectList = ColumnRect.objects.filter()
        #             for columnRect in pageRect.
        #             columnColunt = random.randint(3, 10)
        #             for no in range(0, columnColunt):
        #                 column = ColumnRect.create_columnRect(pageRect, no, random.randint(10, 800), random.randint(10, 600), random.randint(25, 35), random.randint(300, 600))
        #                 columnrects.append(column)
        #         columnTask.status = TaskStatus.COMPLETED
        #         columntasks.append(columnTask)
        # ColumnRect.objects.bulk_create(columnrects)
        # PageTask.objects.bulk_update(pagetasks)
        # # End
        # gen_char_task()


        #gen_discern_task()


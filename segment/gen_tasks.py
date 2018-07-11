
from segment.models import *
from bulk_update.helper import bulk_update
from random import randint

TEST_COLUMN_WIDTH = 50
TEST_CHAR_HEIGHT = 50

#  测试用, 随机抽取部分页去生成页任务数据.
def test_gen_pagerect_test_data():
    pagerectList = PageRect.objects.filter(status=PageRectStatus.CUT_UNCOMPLETED, op=OpStatus.NORMAL)
    pagerects = []
    for pagerect in pagerectList:
        # if (random.randint(0,9) / 3) == 0:
        # 模拟科鑫算法生成页切页数据
        pagerect.update_rect(randint(0, 50), randint(0, 50), randint(600, 750), randint(500, 550))
        pagerects.append(pagerect)
    bulk_update(pagerects)

def gen_pagerect_task():
    pagerectList = PageRect.objects.filter(status=PageRectStatus.CUT_UNCOMPLETED, op=OpStatus.NORMAL)
    # 一页数据生成一个待检查的页数据.
    tasks = []
    i = 0
    for pagerect in pagerectList:
        task = PageTask(number=pagerect.code, schedule=None, owner=None)
        i += 1
        task.gen_number(pagerect.code, i)
        tasks.append(task)
        task.save()
        task.pagerects.add(pagerect)
        task.save()
    #PageTask.objects.bulk_create(tasks)

# 模拟用户做完标注页的任务, 并调用切列算法生成该页任务相关页的切列数据集.
# 测试用, 随机将部分页任务置完成状态去生成列任务数据.
def test_gen_column_task():
    pageTaskList = PageTask.objects.filter(status=TaskStatus.NOT_GOT)
    pagetasks = []
    pagerects = []
    columnrects = []
    for pageTask in pageTaskList:
        if (randint(0, 9) / 2) == 0:
            # 随机模拟页任务完成了
            pageTask.status = TaskStatus.COMPLETED
            pagetasks.append(pageTask)
            pagerectList = pageTask.pagerects.all()
            for pageRect in pagerectList:
                pageRect.op = OpStatus.CHANGED  # 说明页被校对过了.
                pageRect.status = PageRectStatus.CUT_PAGE_COMPLETED
                pagerects.append(pageRect)
                # 模拟算法生成该页的列数据集.
                columnColunt = randint(3, 10)
                for no in range(0, columnColunt):
                    column = ColumnRect.create_Rect(pageRect, no, randint(10, 800), randint(10, 600), TEST_COLUMN_WIDTH, randint(300, 600))
                    columnrects.append(column)

    ColumnRect.objects.bulk_create(columnrects)
    bulk_update(pagerects)
    bulk_update(pagetasks)


def gen_column_task():
    pageTaskList = PageTask.objects.filter(status=TaskStatus.COMPLETED)
    # 一页完成的切页数据对应生成一页的待切列任务.
    for pageTask in pageTaskList:
        if pageTask.pagerects:
            tasks = []
            i = 0
            for pagerect in pageTask.pagerects.all():
                task = ColumnTask(number=pagerect.code, schedule=None, owner=None)
                i += 1
                task.gen_number(pagerect.code, i)
                task.save()
                task.pagerects.add(pagerect)
                task.save()
    #ColumnTask.objects.bulk_create(tasks)

# 模拟用户做完标注列的任务, 并调用切字算法生成该列任务相关页的切字数据集.
def test_gen_char_task():
    columnTaskList = ColumnTask.objects.filter(status=TaskStatus.NOT_GOT)
    columntasks = []
    pagerects = []
    charrects = []
    for columnTask in columnTaskList:
        if (randint(0, 9) / 2) == 0:
            # 随机模拟列任务完成了
            columnTask.status = TaskStatus.COMPLETED
            columntasks.append(columnTask)
            pagerectList = columnTask.pagerects.all()
            for pageRect in pagerectList:
                pageRect.op = OpStatus.CHANGED  # 说明页被校对过了.
                pageRect.status = PageRectStatus.CUT_COLUMN_COMPLETED
                pagerects.append(pageRect)
                # 遍历每一页的所有列数据, 并调用切字算法对这一列的数据进行切字
                columnrectList = ColumnRect.objects.filter(pagerect=pageRect.id)
                for columnRect in columnrectList:
                    # 模拟算法生成该列的切字数据集. 默认每个字高为50, 算出要切多少个字.
                    charCount = int(columnRect.h / TEST_CHAR_HEIGHT)
                    for no in range(0, charCount):
                        char = CharRect.create_Rect(columnRect, no, columnRect.x, columnRect.y+no*TEST_CHAR_HEIGHT, randint(35, TEST_COLUMN_WIDTH), randint(35, TEST_CHAR_HEIGHT))
                        charrects.append(char)

    CharRect.objects.bulk_create(charrects)
    bulk_update(pagerects)
    bulk_update(columntasks)


def gen_char_task():
    pagerectList = PageRect.objects.filter(status=PageRectStatus.CUT_COLUMN_COMPLETED)
    i = 0
    # 一页完成的切列数据集对应生成一页待切字的任务
    for pagerect in pagerectList:
        task = CharTask(number=pagerect.code, schedule=None, owner=None)
        i += 1
        task.gen_number(pagerect.code, i)
        task.save()
        task.pagerects.add(pagerect)
        task.save()

def gen_discern_task():
    charTaskList = CharTask.objects.filter(status=TaskStatus.COMPLETED)
    # 一页完成的切字数据集对应生成一页识别字的任务
    for charTask in charTaskList:
        if charTask.pagerects:
            tasks = []
            for pagerect in charTask.pagerects:
                task = DiscernTask(schedule=None, owner=None)
                task.pagerects.add(pagerect)
                tasks.append(task)
            DiscernTask.objects.bulk_create(tasks)
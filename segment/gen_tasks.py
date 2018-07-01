
from segment.models import *
from bulk_update.helper import bulk_update
from random import randint

#  测试用, 随机抽取部分页去生成页任务数据.
def test_gen_pagerect_test_data():
    pagerectList = PageRect.objects.filter(status=PageRectStatus.CUT_UNCOMPLETED, op=OpStatus.NORMAL)
    pagerects = []
    for pagerect in pagerectList:
        # if (random.randint(0,9) / 3) == 0:
        # 模拟科鑫算法生成页切分数据
        pagerect.update_date(randint(0, 50), randint(0, 50), randint(600, 750), randint(500, 550))
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
                pagerects.append(pageRect)
                # 模拟算法生成该页的列数据集.
                columnColunt = randint(3, 10)
                for no in range(0, columnColunt):
                    column = ColumnRect.create_columnRect(pageRect, no, randint(10, 800), randint(10, 600), randint(25, 35), randint(300, 600))
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
                task = ColumnTask(schedule=None, owner=None)
                i += 1
                task.gen_number(pagerect.code, i)
                task.save()
                task.pagerects.add(pagerect)
                task.save()
    #ColumnTask.objects.bulk_create(tasks)

def gen_char_task():
    columnTaskList = ColumnTask.objects.filter(status=TaskStatus.COMPLETED)
    # 一页完成的切列数据集对应生成一页待切字的任务
    for columnTask in columnTaskList:
        if columnTask.pagerects:
            tasks = []
            for pagerect in columnTask.pagerects:
                task = CharTask(schedule=None, owner=None)
                task.pagerects.add(pagerect)
                tasks.append(task)
            CharTask.objects.bulk_create(tasks)

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
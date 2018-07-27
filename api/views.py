from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from segment.models import *
from django.db.models import Q

@api_view(['GET'])
def task_statistics(request):
    if request.method == 'POST':
        return Response({"code": -1, "message": "Got some data!", "data": request.data})

    pagetask_count = PageTask.objects.count()
    # pagetask_uncompleted = PageTask.objects.filter(status__in=TaskStatus.remain_status)
    pagetask_uncompleted = PageTask.objects.filter(~Q(status=TaskStatus.COMPLETED)).count()
    pagetask_completed = PageTask.objects.filter(status=TaskStatus.COMPLETED).count()
    pagerect_avail = PageRect.objects.filter(status=PageRectStatus.CUT_UNCOMPLETED).count()
    pagerect_completed = PageRect.objects.filter(status__gt=PageRectStatus.CUT_UNCOMPLETED).count()

    columntask_count = ColumnTask.objects.count()
    columntask_uncompleted = ColumnTask.objects.filter(~Q(status=TaskStatus.COMPLETED)).count()
    columntask_completed = ColumnTask.objects.filter(status=TaskStatus.COMPLETED).count()
    columnrect_avail = PageRect.objects.filter(status=PageRectStatus.CUT_PAGE_COMPLETED).count()
    columnrect_completed = PageRect.objects.filter(status__gt=PageRectStatus.CUT_PAGE_COMPLETED).count()

    chartask_count = CharTask.objects.count()
    chartask_uncompleted = CharTask.objects.filter(~Q(status=TaskStatus.COMPLETED)).count()
    chartask_completed = CharTask.objects.filter(status=TaskStatus.COMPLETED).count()
    charrect_avail = PageRect.objects.filter(status=PageRectStatus.CUT_COLUMN_COMPLETED).count()
    charrect_completed = PageRect.objects.filter(status__gt=PageRectStatus.CUT_COLUMN_COMPLETED).count()

    discerntask_count = DiscernTask.objects.count()
    discerntask_uncompleted = DiscernTask.objects.filter(~Q(status=TaskStatus.COMPLETED)).count()
    discerntask_completed = DiscernTask.objects.filter(status=TaskStatus.COMPLETED).count()
    discern_avail = PageRect.objects.filter(status=PageRectStatus.CUT_CHAR_COMPLETED).count()
    discern_completed = PageRect.objects.filter(status__gt=PageRectStatus.CUT_CHAR_COMPLETED).count()

    return Response({"code": 0,
                     "message": "success",
                     "data": [
                         {
                             "task": "pagetask",
                             "name": "页切分标注",
                             "count": pagetask_count,
                             "uncompleted": pagetask_uncompleted,
                             "completed": pagetask_completed,
                             "rect_avail": pagerect_avail,
                             "rect_completed": pagerect_completed
                         },
                         {
                             "task": "columntask",
                             "name": "列切分标注",
                             "count": columntask_count,
                             "uncompleted": columntask_uncompleted,
                             "completed": columntask_completed,
                             "rect_avail": columnrect_avail,
                             "rect_completed": columnrect_completed
                         },
                         {
                             "task": "chartask",
                             "name": "字切分标注",
                             "count": chartask_count,
                             "uncompleted": chartask_uncompleted,
                             "completed": chartask_completed,
                             "rect_avail": charrect_avail,
                             "rect_completed": charrect_completed
                         },
                         {
                             "task": "discerntask",
                             "name": "文本识别标注",
                             "count": discerntask_count,
                             "uncompleted": discerntask_uncompleted,
                             "completed": discerntask_completed,
                             "rect_avail": discern_avail,
                             "rect_completed": discern_completed
                         }
                     ]
                })


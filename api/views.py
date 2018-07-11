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

    columntask_count = ColumnTask.objects.count()
    columntask_uncompleted = ColumnTask.objects.filter(~Q(status=TaskStatus.COMPLETED)).count()
    columntask_completed = ColumnTask.objects.filter(status=TaskStatus.COMPLETED).count()

    chartask_count = CharTask.objects.count()
    chartask_uncompleted = CharTask.objects.filter(~Q(status=TaskStatus.COMPLETED)).count()
    chartask_completed = CharTask.objects.filter(status=TaskStatus.COMPLETED).count()

    discerntask_count = DiscernTask.objects.count()
    discerntask_uncompleted = DiscernTask.objects.filter(~Q(status=TaskStatus.COMPLETED)).count()
    discerntask_completed = DiscernTask.objects.filter(status=TaskStatus.COMPLETED).count()

    return Response({"code": 0,
                     "message": "success",
                     "data": {
                         "pagetask":{
                             "count": pagetask_count,
                             "uncompleted": pagetask_uncompleted,
                             "completed": pagetask_completed
                         },
                         "columntask": {
                             "count": columntask_count,
                             "uncompleted": columntask_uncompleted,
                             "completed": columntask_completed
                         },
                         "chartask": {
                             "count": chartask_count,
                             "uncompleted": chartask_uncompleted,
                             "completed": chartask_completed
                         },
                         "discerntask": {
                             "count": discerntask_count,
                             "uncompleted": discerntask_uncompleted,
                             "completed": discerntask_completed
                         }
                     }})


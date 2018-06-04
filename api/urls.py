# -*- coding: UTF-8 -*-
from django.conf.urls import url, include
from django.urls import include, path
from rest_framework import routers

from tdata.views import PageViewSet
from segment.views import PageRectViewSet, ColumnRectViewSet, CharRectViewSet, \
                            ScheduleViewSet, PageTaskViewSet, ColumnTaskViewSet, CharTaskViewSet, DiscernTaskViewSet


rectRouter = routers.DefaultRouter()
rectRouter.register(r'pagerect', PageRectViewSet)
rectRouter.register(r'columnrect', ColumnRectViewSet)
rectRouter.register(r'charrect', CharRectViewSet)

rectRouter.register(r'schedule', ScheduleViewSet)

rectRouter.register(r'pagetask', PageTaskViewSet)
rectRouter.register(r'columntask', ColumnTaskViewSet)
rectRouter.register(r'chartask', CharTaskViewSet)
rectRouter.register(r'discerntask', DiscernTaskViewSet)

urlpatterns = [
    url(r'^', include(rectRouter.urls)),
]
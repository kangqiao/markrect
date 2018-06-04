from django.shortcuts import render

from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from segment.models import * 
from segment.serializers import *
from api.pagination import StandardPagination


# Create your views here.
class RectResultsSetPagination(StandardPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


##########################################
####  切分模块                        #####
##########################################
class PageRectViewSet(viewsets.ModelViewSet):
    queryset = PageRect.objects.all()
    serializer_class = PageRectSerializer
    pagination_class = RectResultsSetPagination


class ColumnRectViewSet(viewsets.ModelViewSet):
    queryset = ColumnRect.objects.all()
    serializer_class = ColumnRectSerializer
    #pagination_class = RectResultsSetPagination

class CharRectViewSet(viewsets.ModelViewSet):
    queryset = CharRect.objects.all()
    serializer_class = CharRectSerializer
    #pagination_class = RectResultsSetPagination


##########################################
####  任务模块                        #####
##########################################
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    pagination_class = RectResultsSetPagination


class PageTaskViewSet(viewsets.ModelViewSet):
    queryset = PageTask.objects.all()
    serializer_class = PageTaskSerializer
    #pagination_class = RectResultsSetPagination


class ColumnTaskViewSet(viewsets.ModelViewSet):
    queryset = ColumnTask.objects.all()
    serializer_class = ColumnTaskSerializer
    #pagination_class = RectResultsSetPagination


class CharTaskViewSet(viewsets.ModelViewSet):
    queryset = CharTask.objects.all()
    serializer_class = CharTaskSerializer
    #pagination_class = RectResultsSetPagination


class DiscernTaskViewSet(viewsets.ModelViewSet):
    queryset = DiscernTask.objects.all()
    serializer_class = DiscernTaskSerializer
    #pagination_class = RectResultsSetPagination
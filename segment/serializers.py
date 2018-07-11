# -*- coding: UTF-8 -*-

from segment.models import *
from rest_framework import serializers

##########################################
####  切分模块                        #####
##########################################
class ColumnRectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColumnRect
        fields = '__all__'


class CharRectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharRect
        fields = '__all__'


class PageRectSerializer(serializers.ModelSerializer):
    #char_rects = CharRectSerializer(many=True)

    def to_representation(self, instance):
        '''
            to_representation 将从 Model 取出的数据 parse 给 Api
            to_internal_value 将客户端传来的 json 数据 parse 给 Model
            当请求版本列表时, 不显示版本的目录信息.
            参考: https://github.com/dbrgn/drf-dynamic-fields/blob/master/drf_dynamic_fields/__init__.py
        '''
        request = self.context['request']
        if request.resolver_match.url_name == 'pagerect-list' and 'char_rects' in self.fields:
            self.fields.pop('char_rects')
        return super().to_representation(instance)

    class Meta:
        model = PageRect
        fields = '__all__'


##########################################
####  任务模块                        #####
##########################################
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class PageTaskSerializer(serializers.ModelSerializer):
    pagerects = PageRectSerializer(many=True)
    class Meta:
        model = PageTask
        fields = '__all__'


class ColumnTaskSerializer(serializers.ModelSerializer):
    pagerects = PageRectSerializer(many=True)
    #column_set = ColumnRectSerializer(many=True)
    class Meta:
        model = ColumnTask
        fields = '__all__'


class CharTaskSerializer(serializers.ModelSerializer):
    pagerects = PageRectSerializer(many=True)
    #char_set = CharRectSerializer(many=True)
    class Meta:
        model = CharTask
        fields = '__all__'


class DiscernTaskSerializer(serializers.ModelSerializer):
    pagerects = PageRectSerializer(many=True)
    #char_set = CharRectSerializer(many=True)
    class Meta:
        model = DiscernTask
        fields = '__all__'
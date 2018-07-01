

from functools import wraps
import os, sys
import uuid

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.db import connection, transaction
from django.db.models import Sum, Case, When, Value, Count, Avg, F
from django.db.models import Min, Sum, Case, When, Value, Count, F
from django.db import connection, transaction
from django.dispatch import receiver
from django_bulk_update.manager import BulkUpdateManager
from django.forms.models import model_to_dict
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.utils.timezone import localtime, now

from PIL import Image, ImageFont, ImageDraw
from celery import shared_task

from jwt_auth.models import Staff
from tdata.models import Page, Reel
from utils.lib.fields import JSONField
import inspect


# Create your models here.
##########################################
####  切分模块                        #####
##########################################
class OpStatus(object):
    NORMAL = 1
    CHANGED = 2
    DELETED = 3
    RECOG = 4
    COLLATE = 5
    CHOICES = (
        (NORMAL, u'正常'), #初始状态, 未被人工校对过的.
        (CHANGED, u'被更改'),
        (DELETED, u'被删除'),
        (RECOG, u'文字识别'),
        (COLLATE, u'文字校对')
    )

class PageRectStatus(object):
    CUT_UNCOMPLETED = 0
    CUT_PAGE_COMPLETED = 1
    CUT_COLUMN_COMPLETED = 2
    CUT_CHAR_COMPLETED = 3
    COMPLETED = 4

    CHOICES = (
        (CUT_UNCOMPLETED, u'未开始'),
        (CUT_PAGE_COMPLETED, u'页切分完成'),
        (CUT_COLUMN_COMPLETED, u'列切分完成'),
        (CUT_CHAR_COMPLETED, u'字切分完成'),
        (COMPLETED, u'字标识完成'),
    )
'''
根据最新编码规则生成的三种藏经图片存储命名示例
页, 列, 字的编码规范. 贤度法师定的, 应保持统一, 请OCR生成时注意规范.
https://tower.im/projects/3032432a1c5b4618a668509f25448034/messages/419ecfb3901e4faba2574447ce8cc7f6/
'''
class Rect(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    
    updated_at = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    op = models.PositiveSmallIntegerField(verbose_name=u'操作类型', default=OpStatus.NORMAL)
    x = models.PositiveSmallIntegerField(verbose_name=u'X坐标', default=0)
    y = models.PositiveSmallIntegerField(verbose_name=u'Y坐标', default=0)
    w = models.IntegerField(verbose_name=u'宽度', null=True, blank=True)
    h = models.IntegerField(verbose_name=u'高度', null=True, blank=True)

    @property
    def s3_uri(self):
        return '%s%s%s.jpg' % (settings.IMAGE_URL_PREFIX, self.reel.url_prefix(), self.page_no)

    class Meta:
        abstract = True
        verbose_name = u"切分块"
        verbose_name_plural = u"切分块基础描述"
        ordering = ("id", "code")
        indexes = [
            models.Index(fields=['id', 'code']),
        ]

class PageRect(Rect):
    code = models.CharField(verbose_name=u'页编号', max_length=21, blank=False, unique=True)
    img_path = models.CharField(verbose_name=u'页url路径', max_length=21, blank=False)
    page = models.OneToOneField(Page, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='pagerect', verbose_name=u'实体页')
    #reel_code = models.CharField(verbose_name=u'所属卷code编码', max_length=21, blank=False)
    status = models.PositiveSmallIntegerField(
        db_index=True,
        choices=PageRectStatus.CHOICES,
        default=PageRectStatus.CUT_UNCOMPLETED,
        verbose_name=u'切分标注状态',
    )
    text = models.TextField('整页文本', default='', blank=True)
    rect_set = JSONField(default=list, verbose_name=u'字块JSON切分数据集', blank=True)

    def update_date(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


    def img_url(self):
        # https://s3.cn-north-1.amazonaws.com.cn/lqdzj-image/YB/19/YB_19_644.jpg
        img_url = "%s/%s.jpg" % (settings.IMAGE_URL_PREFIX, self.img_path)
        return img_url


    class Meta:
        verbose_name = u"页块"
        verbose_name_plural = u"页的切分数据"
    
class ColumnRect(Rect):
    code = models.CharField(verbose_name='列编号', max_length=21, blank=False, unique=True)
    pagerect = models.ForeignKey(PageRect, null=True, blank=True, related_name='column_rects', on_delete=models.SET_NULL, verbose_name=u'页块')
    column_no = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'列号', default=0)  # 对应图片的一列

    def gen_code(self, no):
        if self.pagerect:
            self.column_no = int(no)
            self.code = self.pagerect.code + "_L" + str(no)

    @staticmethod
    def create_columnRect(pagerect, no, x, y, w, h):
        if pagerect:
            column = ColumnRect(pagerect=pagerect)
            column.gen_code(no)
            column.x = x
            column.y = y
            column.w = w
            column.h = h
            return column
        return None

    def column_uri(self):
        return ColumnRect.column_uri_path(self.code)

    @staticmethod
    def column_uri_path(col_s3_id):
        col_id = str(col_s3_id)
        col_path = col_id.replace('_', '/')
        return '%s/%s/%s.jpg' % (settings.COL_IMAGE_URL_PREFIX, os.path.dirname(col_path), col_id)

    class Meta:
        verbose_name = u"列块"
        verbose_name_plural = u"页的列切分数据"

class CharRect(Rect):
    code = models.CharField(verbose_name='字编号', max_length=21, blank=False, unique=True)
    pagerect = models.ForeignKey(PageRect, null=True, blank=True, related_name='char_rects', on_delete=models.SET_NULL, verbose_name=u'页块')
    column_no = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'列号', default=0)  # 对应图片的一列
    char_no = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'字号', default=0)
    cc = models.FloatField(null=True, blank=True, verbose_name=u'切分置信度', default=1) #是否需要了.
    ch = models.CharField(null=True, blank=True, verbose_name=u'文字', max_length=2, default='') #ocr识别的, 或者上一次校对的结果.
    ts = models.CharField(null=True, blank=True, verbose_name=u'标字', max_length=2, default='') #校对后的

    @staticmethod
    def create_charRect(columnRect, no, x, y, w, h):
        if columnRect:
            char = CharRect(pagerect=columnRect.pagerect, column_no=columnRect.column_no)
            char.gen_code(no)
            char.x = x
            char.y = y
            char.w = w
            char.h = h
            return char
        return None

    class Meta:
        verbose_name = u"字块"
        verbose_name_plural = u"页的字切分数据"


##########################################
####  任务模块                        #####
##########################################
class ScheduleStatus:
    NOT_ACTIVE = 0
    ACTIVE = 1
    EXPIRED = 2
    DISCARD = 3
    COMPLETED = 4
    CHOICES = (
        (NOT_ACTIVE, u'未激活'),
        (ACTIVE, u'已激活'),
        (EXPIRED, u'已过期'),
        (DISCARD, u'已作废'),
        (COMPLETED, u'已完成'),
    )


class TaskStatus:
    NOT_GOT = 0
    EXPIRED = 1
    ABANDON = 2
    HANDLING = 4
    COMPLETED = 5
    DISCARD = 6

    CHOICES = (
        (NOT_GOT, u'未领取'),
        (EXPIRED, u'已过期'),
        (ABANDON, u'已放弃'),
        (HANDLING, u'处理中'),
        (COMPLETED, u'已完成'),
        (DISCARD, u'已作废'),
    )
    #未完成状态.
    remain_status = [NOT_GOT, EXPIRED, ABANDON, HANDLING]

class PriorityLevel:
    LOW = 1
    MIDDLE = 3
    HIGH = 5
    HIGHEST = 7

    CHOICES = (
        (LOW, u'低'),
        (MIDDLE, u'中'),
        (HIGH, u'高'),
        (HIGHEST, u'最高'),
    )

class ActivityLog(models.Model):
    user = models.ForeignKey(Staff, related_name='activities', on_delete=models.SET_NULL, null=True)
    log = models.CharField(verbose_name=u'记录', max_length=128, default='')
    object_type = models.CharField(verbose_name=u'对象类型', max_length=32)
    object_pk = models.CharField(verbose_name=u'对象主键', max_length=64)
    action = models.CharField(verbose_name=u'行为', max_length=16)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    def log_message(self):
        return "User:%s %s to %s(%s) at %s" % (self.user.id,
                                               self.action, self.object_type,
                                               self.object_pk, self.created_at)


def activity_log(func):
    @wraps(func)
    def tmp(*args, **kwargs):
        result = func(*args, **kwargs)
        self = args[0]
        ActivityLog.objects.create(user=self.owner, object_pk=self.pk,
                                    object_type=type(self).__name__,
                                    action=func.__name__)
        return result
    return tmp


class Schedule(models.Model):
    '''
    切分标注计划
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reels = models.ManyToManyField(Reel, limit_choices_to={'image_ready': True}, blank=True)
    alloc_config = models.CharField(verbose_name='任务分配配置及策略', max_length=64)
    name = models.CharField(verbose_name='计划名称', max_length=64)
    # todo 设置总任务的优先级时, 子任务包的优先级凡是小于总任务优先级的都提升优先级, 高于或等于的不处理. 保持原优先级.
    priority = models.PositiveSmallIntegerField(
        choices=PriorityLevel.CHOICES,
        default=PriorityLevel.MIDDLE,
        verbose_name=u'任务计划优先级',
    )
    status = models.PositiveSmallIntegerField(
        db_index=True,
        null=True,
        blank=True,
        choices=ScheduleStatus.CHOICES,
        default=ScheduleStatus.NOT_ACTIVE,
        verbose_name=u'计划状态',
    )
    due_at = models.DateField(null=True, blank=True, verbose_name=u'截止日期')
    created_at = models.DateTimeField(null=True, blank=True, verbose_name=u'创建日期', auto_now_add=True)
    remark = models.TextField(max_length=256, null=True, blank=True, verbose_name=u'备注')
    schedule_no = models.CharField(max_length=64, verbose_name=u'切分计划批次', default='', help_text=u'自动生成', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"切分计划"
        verbose_name_plural = u"切分计划管理"
        ordering = ('due_at', "status")


class Task(models.Model):
    number = models.CharField(primary_key=True, max_length=64, verbose_name='任务编号')
    desc = models.TextField(null=True, blank=True, verbose_name=u'任务格式化描述')
    status = models.PositiveSmallIntegerField(
        db_index=True,
        choices=TaskStatus.CHOICES,
        default=TaskStatus.NOT_GOT,
        verbose_name=u'任务状态',
    )
    priority = models.PositiveSmallIntegerField(
        choices=PriorityLevel.CHOICES,
        default=PriorityLevel.MIDDLE,
        verbose_name=u'任务优先级',
        db_index=True,
    )
    update_date = models.DateField(null=True, verbose_name=u'最近处理时间', auto_now=True)

    def __str__(self):
        return self.number

    @classmethod
    def serialize_set(cls, dataset):
        return ";".join(dataset)

    @activity_log
    def done(self):
        self.status = TaskStatus.COMPLETED
        self.tasks_increment()
        return self.save(update_fields=["status"])

    @activity_log
    def abandon(self):
        self.status = TaskStatus.ABANDON
        return self.save(update_fields=["status"])

    @activity_log
    def expire(self):
        self.status = TaskStatus.EXPIRED
        return self.save(update_fields=["status"])

    @activity_log
    def obtain(self, user):
        self.update_date = localtime(now()).date()
        self.status = TaskStatus.HANDLING
        self.owner = user
        self.save()

    def gen_number(self, code, no):
        self.number = code + "_T" + str(no)

    class Meta:
        abstract = True
        verbose_name = u"切分任务"
        verbose_name_plural = u"切分任务管理"
        ordering = ("priority", "status")
        indexes = [
            models.Index(fields=['priority', 'status']),
        ]

class PageTask(Task):
    schedule = models.ForeignKey(Schedule, null=True, blank=True, related_name='page_tasks', on_delete=models.SET_NULL, verbose_name=u'切分计划')
    owner = models.ForeignKey(Staff, null=True, blank=True, related_name='page_tasks', on_delete=models.SET_NULL, verbose_name=u'处理人')
    pagerects = models.ManyToManyField(PageRect, limit_choices_to={'status': PageRectStatus.CUT_UNCOMPLETED}, blank=True )
    page_set = JSONField(default=list, verbose_name=u'字块集') # [pagerect_id, {格式化好的页相关数据} ?是否需要]

    class Meta:
        verbose_name = u"页切分标注任务"
        verbose_name_plural = u"页切分标注任务管理"

class ColumnTask(Task):
    schedule = models.ForeignKey(Schedule, null=True, blank=True, related_name='column_tasks', on_delete=models.SET_NULL, verbose_name=u'切分计划')
    owner = models.ForeignKey(Staff, null=True, blank=True, related_name='column_tasks', on_delete=models.SET_NULL, verbose_name=u'处理人')
    pagerects = models.ManyToManyField(PageRect, limit_choices_to={'status': PageRectStatus.CUT_PAGE_COMPLETED}, blank=True )
    column_set = JSONField(default=list, verbose_name=u'字块集') # [pagerect_id, {格式化好的页相关数据} ?是否需要]

    class Meta:
        verbose_name = u"列切分标注任务"
        verbose_name_plural = u"列切分标注任务管理"

class CharTask(Task):
    schedule = models.ForeignKey(Schedule, null=True, blank=True, related_name='char_tasks', on_delete=models.SET_NULL, verbose_name=u'切分计划')
    owner = models.ForeignKey(Staff, null=True, blank=True, related_name='char_tasks', on_delete=models.SET_NULL, verbose_name=u'处理人')
    pagerects = models.ManyToManyField(PageRect, limit_choices_to={'status': PageRectStatus.CUT_COLUMN_COMPLETED}, blank=True )
    char_set = JSONField(default=list, verbose_name=u'字块集') # [pagerect_id, {格式化好的页相关数据} ?是否需要]

    class Meta:
        verbose_name = u"字框切分标注任务"
        verbose_name_plural = u"字框切分标注任务管理"

class DiscernTask(Task):
    schedule = models.ForeignKey(Schedule, null=True, blank=True, related_name='discern_tasks', on_delete=models.SET_NULL, verbose_name=u'切分计划')
    owner = models.ForeignKey(Staff, null=True, blank=True, related_name='discern_tasks', on_delete=models.SET_NULL, verbose_name=u'处理人')
    pagerects = models.ManyToManyField(PageRect, limit_choices_to={'status': PageRectStatus.CUT_CHAR_COMPLETED}, blank=True )
    char_set = JSONField(default=list, verbose_name=u'字块集') # [pagerect_id, {格式化好的页相关数据} ?是否需要]

    class Meta:
        verbose_name = u"文本识别标注任务"
        verbose_name_plural = u"文本识别标注任务管理"


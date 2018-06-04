# Generated by Django 2.0.2 on 2018-06-03 16:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.lib.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tdata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log', models.CharField(default='', max_length=128, verbose_name='记录')),
                ('object_type', models.CharField(max_length=32, verbose_name='对象类型')),
                ('object_pk', models.CharField(max_length=64, verbose_name='对象主键')),
                ('action', models.CharField(max_length=16, verbose_name='行为')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activities', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CharRect',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('op', models.PositiveSmallIntegerField(default=1, verbose_name='操作类型')),
                ('x', models.PositiveSmallIntegerField(default=0, verbose_name='X坐标')),
                ('y', models.PositiveSmallIntegerField(default=0, verbose_name='Y坐标')),
                ('w', models.IntegerField(blank=True, null=True, verbose_name='宽度')),
                ('h', models.IntegerField(blank=True, null=True, verbose_name='高度')),
                ('code', models.CharField(max_length=21, unique=True, verbose_name='字编号')),
                ('column_no', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='列号')),
                ('char_no', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='字号')),
                ('cc', models.FloatField(blank=True, default=1, null=True, verbose_name='切分置信度')),
                ('ch', models.CharField(blank=True, default='', max_length=2, null=True, verbose_name='文字')),
                ('ts', models.CharField(blank=True, default='', max_length=2, null=True, verbose_name='标字')),
            ],
            options={
                'verbose_name': '字块',
                'verbose_name_plural': '页的字切分数据',
            },
        ),
        migrations.CreateModel(
            name='CharTask',
            fields=[
                ('number', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='任务编号')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='任务格式化描述')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, '未领取'), (1, '已过期'), (2, '已放弃'), (4, '处理中'), (5, '已完成'), (6, '已作废')], db_index=True, default=0, verbose_name='任务状态')),
                ('priority', models.PositiveSmallIntegerField(choices=[(1, '低'), (3, '中'), (5, '高'), (7, '最高')], db_index=True, default=3, verbose_name='任务优先级')),
                ('update_date', models.DateField(null=True, verbose_name='最近处理时间')),
                ('page_set', utils.lib.fields.JSONField(default=list, verbose_name='字块集')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='char_tasks', to=settings.AUTH_USER_MODEL, verbose_name='处理人')),
            ],
            options={
                'verbose_name': '字框切分标注任务',
                'verbose_name_plural': '字框切分标注任务管理',
            },
        ),
        migrations.CreateModel(
            name='ColumnRect',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('op', models.PositiveSmallIntegerField(default=1, verbose_name='操作类型')),
                ('x', models.PositiveSmallIntegerField(default=0, verbose_name='X坐标')),
                ('y', models.PositiveSmallIntegerField(default=0, verbose_name='Y坐标')),
                ('w', models.IntegerField(blank=True, null=True, verbose_name='宽度')),
                ('h', models.IntegerField(blank=True, null=True, verbose_name='高度')),
                ('code', models.CharField(max_length=21, unique=True, verbose_name='列编号')),
                ('column_no', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='列号')),
            ],
            options={
                'verbose_name': '列块',
                'verbose_name_plural': '页的列切分数据',
            },
        ),
        migrations.CreateModel(
            name='ColumnTask',
            fields=[
                ('number', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='任务编号')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='任务格式化描述')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, '未领取'), (1, '已过期'), (2, '已放弃'), (4, '处理中'), (5, '已完成'), (6, '已作废')], db_index=True, default=0, verbose_name='任务状态')),
                ('priority', models.PositiveSmallIntegerField(choices=[(1, '低'), (3, '中'), (5, '高'), (7, '最高')], db_index=True, default=3, verbose_name='任务优先级')),
                ('update_date', models.DateField(null=True, verbose_name='最近处理时间')),
                ('page_set', utils.lib.fields.JSONField(default=list, verbose_name='字块集')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='column_tasks', to=settings.AUTH_USER_MODEL, verbose_name='处理人')),
            ],
            options={
                'verbose_name': '列切分标注任务',
                'verbose_name_plural': '列切分标注任务管理',
            },
        ),
        migrations.CreateModel(
            name='DiscernTask',
            fields=[
                ('number', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='任务编号')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='任务格式化描述')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, '未领取'), (1, '已过期'), (2, '已放弃'), (4, '处理中'), (5, '已完成'), (6, '已作废')], db_index=True, default=0, verbose_name='任务状态')),
                ('priority', models.PositiveSmallIntegerField(choices=[(1, '低'), (3, '中'), (5, '高'), (7, '最高')], db_index=True, default=3, verbose_name='任务优先级')),
                ('update_date', models.DateField(null=True, verbose_name='最近处理时间')),
                ('page_set', utils.lib.fields.JSONField(default=list, verbose_name='字块集')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='discern_tasks', to=settings.AUTH_USER_MODEL, verbose_name='处理人')),
            ],
            options={
                'verbose_name': '文本识别标注任务',
                'verbose_name_plural': '文本识别标注任务管理',
            },
        ),
        migrations.CreateModel(
            name='PageRect',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('op', models.PositiveSmallIntegerField(default=1, verbose_name='操作类型')),
                ('x', models.PositiveSmallIntegerField(default=0, verbose_name='X坐标')),
                ('y', models.PositiveSmallIntegerField(default=0, verbose_name='Y坐标')),
                ('w', models.IntegerField(blank=True, null=True, verbose_name='宽度')),
                ('h', models.IntegerField(blank=True, null=True, verbose_name='高度')),
                ('code', models.CharField(max_length=21, unique=True, verbose_name='页编号')),
                ('img_path', models.CharField(max_length=21, verbose_name='页url路径')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, '未开始'), (1, '页切分完成'), (2, '列切分完成'), (3, '字切分完成'), (4, '字标识完成')], db_index=True, default=0, verbose_name='切分标注状态')),
                ('text', models.TextField(blank=True, default='', verbose_name='整页文本')),
                ('rect_set', utils.lib.fields.JSONField(blank=True, default=list, verbose_name='字块JSON切分数据集')),
                ('page', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pagerect', to='tdata.Page', verbose_name='实体页')),
            ],
            options={
                'verbose_name': '页块',
                'verbose_name_plural': '页的切分数据',
            },
        ),
        migrations.CreateModel(
            name='PageTask',
            fields=[
                ('number', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='任务编号')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='任务格式化描述')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, '未领取'), (1, '已过期'), (2, '已放弃'), (4, '处理中'), (5, '已完成'), (6, '已作废')], db_index=True, default=0, verbose_name='任务状态')),
                ('priority', models.PositiveSmallIntegerField(choices=[(1, '低'), (3, '中'), (5, '高'), (7, '最高')], db_index=True, default=3, verbose_name='任务优先级')),
                ('update_date', models.DateField(null=True, verbose_name='最近处理时间')),
                ('page_set', utils.lib.fields.JSONField(default=list, verbose_name='字块集')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='page_tasks', to=settings.AUTH_USER_MODEL, verbose_name='处理人')),
                ('pagerects', models.ManyToManyField(blank=True, limit_choices_to={'status': 0}, to='segment.PageRect')),
            ],
            options={
                'verbose_name': '页切分标注任务',
                'verbose_name_plural': '页切分标注任务管理',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('alloc_config', models.CharField(max_length=64, verbose_name='任务分配配置及策略')),
                ('name', models.CharField(max_length=64, verbose_name='计划名称')),
                ('priority', models.PositiveSmallIntegerField(choices=[(1, '低'), (3, '中'), (5, '高'), (7, '最高')], default=3, verbose_name='任务计划优先级')),
                ('status', models.PositiveSmallIntegerField(blank=True, choices=[(0, '未激活'), (1, '已激活'), (2, '已过期'), (3, '已作废'), (4, '已完成')], db_index=True, default=0, null=True, verbose_name='计划状态')),
                ('due_at', models.DateField(blank=True, null=True, verbose_name='截止日期')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建日期')),
                ('remark', models.TextField(blank=True, max_length=256, null=True, verbose_name='备注')),
                ('schedule_no', models.CharField(blank=True, default='', help_text='自动生成', max_length=64, verbose_name='切分计划批次')),
                ('reels', models.ManyToManyField(blank=True, limit_choices_to={'image_ready': True}, to='tdata.Reel')),
            ],
            options={
                'verbose_name': '切分计划',
                'verbose_name_plural': '切分计划管理',
                'ordering': ('due_at', 'status'),
            },
        ),
        migrations.AddField(
            model_name='pagetask',
            name='schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='page_tasks', to='segment.Schedule', verbose_name='切分计划'),
        ),
        migrations.AddField(
            model_name='discerntask',
            name='pagerects',
            field=models.ManyToManyField(blank=True, limit_choices_to={'status': 3}, to='segment.PageRect'),
        ),
        migrations.AddField(
            model_name='discerntask',
            name='schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='discern_tasks', to='segment.Schedule', verbose_name='切分计划'),
        ),
        migrations.AddField(
            model_name='columntask',
            name='pagerects',
            field=models.ManyToManyField(blank=True, limit_choices_to={'status': 1}, to='segment.PageRect'),
        ),
        migrations.AddField(
            model_name='columntask',
            name='schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='column_tasks', to='segment.Schedule', verbose_name='切分计划'),
        ),
        migrations.AddField(
            model_name='columnrect',
            name='pagerect',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='column_rects', to='segment.PageRect', verbose_name='页块'),
        ),
        migrations.AddField(
            model_name='chartask',
            name='pagerects',
            field=models.ManyToManyField(blank=True, limit_choices_to={'status': 2}, to='segment.PageRect'),
        ),
        migrations.AddField(
            model_name='chartask',
            name='schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='char_tasks', to='segment.Schedule', verbose_name='切分计划'),
        ),
        migrations.AddField(
            model_name='charrect',
            name='pagerect',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='char_rects', to='segment.PageRect', verbose_name='页块'),
        ),
    ]
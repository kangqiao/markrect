import xadmin
from xadmin import views
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, ListAdminView
from xadmin.plugins.actions import BaseActionView
from xadmin.views.base import filter_hook
from django.template.response import TemplateResponse
from django.template import loader

from tdata.models import *
#from tasks.models import Task, CorrectFeedback, JudgeFeedback, LQPunctFeedback, \
#AbnormalLineCountTask ,BatchTask
#from rect.models import *
from jwt_auth.models import Staff
#from tasks.task_controller import correct_update_async, regenerate_correctseg_async

# 龙泉经目 LQSutra


class LQSutraAdmin(object):
    list_display = ['sid', 'variant_code', 'name', 'author',
                    'total_reels', 'remark', 'showSutra']  # 自定义显示这两个字段

    def showSutra(self, obj):
        return '<a href="/xadmin/tdata/sutra/?_p_lqsutra__id__in='+str(obj.id)+'">查看版本</a>'
        # return '<a href="/xadmin/sutradata/sutra/?">查看版本</a>'
    showSutra.short_description = u'操作'
    showSutra.allow_tags = True

    search_fields = ['sid', 'name', 'author']
    list_filter = ['sid', 'name', 'author']
    ordering = ['sid', ]  # 按照倒序排列  -号是倒序

# 实体藏 Tripitaka


class TripitakaAdmin(object):
    list_display = ['id', 'name', 'code', 'operator', 'path1_char',
                    'path1_name', 'path2_char', 'path2_name', 'path3_char', 'path3_name']

    def operator(self, obj):
        edit = '<a href="/xadmin/sutradata/tripitaka/' + \
            str(obj.id)+'/update/">修改</a> '
        dele = '<a href="/xadmin/sutradata/tripitaka/' + \
            str(obj.id)+'/delete/">删除</a> '
        return edit+dele
    operator.short_description = u'操作'
    operator.allow_tags = True
    # search_fields = ['question_text','pub_date'] #可以搜索的字段
    # list_filter = ['question_text','pub_date']
    ordering = ['id', ]  # 按照倒序排列


# 实体经  Sutra
class SutraAdmin(object):
    list_display = ['tripitaka', 'name', 'total_reels', 'Real_reels', 'sid',
                    'lqsutra_name', 'lqsutra_sid', 'remark', 'operator']  # 自定义显示这两个字段

    def Real_reels(self, obj):
        return Reel.objects.filter(sutra=obj.id).count()

    def operator(self, obj):
        edit = '<a href="/xadmin/sutradata/sutra/' + \
            str(obj.id)+'/update/">修改</a> '
        dele = '<a href="/xadmin/sutradata/sutra/' + \
            str(obj.id)+'/delete/">删除</a> '
        return edit+dele
    operator.short_description = u'操作'
    operator.allow_tags = True

    def lqsutra_sid(self, obj):
        if obj == None:
            return
        line = obj.lqsutra.__str__()
        line_list = line.split(':')
        return line_list[0]

    def lqsutra_name(self, obj):
        line = obj.lqsutra.__str__()
        line_list = line.split(':')
        if len(line_list) < 2:
            return
        return line_list[1]
    lqsutra_sid.short_description = u'龙泉编码'
    lqsutra_name.short_description = u'龙泉经名'
    Real_reels.short_description = u'实存卷数'
    # tripitaka.short_description=u'藏'
    list_select_related = False

    search_fields = ['name', 'tripitaka__name', 'tripitaka__code', 'lqsutra__id',
                     'sid', 'total_reels', 'remark']  # 可以搜索的字段
    free_query_filter = True
    list_filter = ['name', 'lqsutra__id', 'sid', 'remark']
    list_display_links = ('name')
    fields = ('tripitaka', 'sid', 'name', 'total_reels', 'remark')
    ordering = ['id', ]  # 按照倒序排列


class VolumeAdmin(object):
    list_display = ['tripitaka_name', 'vol_no', 'page_count']  # 自定义显示这两个字段

    def tripitaka_name(self, obj):  # 藏名
        t = Tripitaka.objects.get(code=obj.tripitaka.code)
        s = t.__str__()
        return t
    tripitaka_name.short_description = u'藏名'

# class RegenerateCorrectSegAction(BaseActionView):
#
#     action_name = "regenerate_correctseg"
#     description = '重新生成文字校对任务的数据（新增页）'
#     icon = 'fa fa-refresh'
#
#     @filter_hook
#     def do_action(self, queryset):
#         reel_id_lst = []
#         for reel in queryset:
#             reel_id_lst.append(reel.id)
#         reel_id_lst_json = json.dumps(reel_id_lst)
#         regenerate_correctseg_async(reel_id_lst_json)
#         if reel_id_lst:
#             self.message_user("成功对%(count)d卷重新生成了文字校对任务的数据。" % {
#                 "count": len(reel_id_lst),
#             }, 'success')

class ReelAdmin(object):
    list_display = ['tripitaka_name', 'sutra_name', 'reel_no', 'longquan_Name', 'remark',
                    'start_vol', 'start_vol_page', 'end_vol', 'end_vol_page',
                    'image_ready', 'cut_ready', 'column_ready', 'ocr_ready', 'correct_ready']  # 自定义显示这两个字段

    def tripitaka_name(self, obj):  # 藏名
        t = Tripitaka.objects.get(code=obj.sutra.tripitaka.code)
        s = t.__str__()
        return t

    def longquan_Name(self, obj):  # 龙泉经名
        return obj.sutra.lqsutra.name

    def sutra_name(self, obj):
        return obj.sutra.name

    sutra_name.short_description = u'经名'
    tripitaka_name.short_description = u'藏名'
    longquan_Name.short_description = u'龙泉经名'
    search_fields = ['sutra__sid', 'sutra__name', 'sutra__tripitaka__name',  'sutra__tripitaka__code',
                     '=reel_no', 'remark']  # 可以搜索的字段
    list_filter = ['sutra__sid', 'sutra__name', 'ocr_ready', 'correct_ready']
    ordering = ['id', 'reel_no']  # 按照倒序排列
    fields = ('sutra', 'reel_no', 'remark',
              'start_vol', 'start_vol_page', 'end_vol', 'end_vol_page')
    list_display_links = ('sutra_name')
    #actions = [RegenerateCorrectSegAction]

class ConfigurationAdmin:
    def modify(self, instance):
        return '修改'
    modify.short_description = '操作'
    list_display = ['task_timeout', 'modify']
    list_display_links = ("modify",)
    remove_permissions = ['add', 'delete']

xadmin.site.register(LQSutra, LQSutraAdmin)
xadmin.site.register(Tripitaka, TripitakaAdmin)
xadmin.site.register(Volume, VolumeAdmin)
xadmin.site.register(Sutra, SutraAdmin)
xadmin.site.register(Reel, ReelAdmin)
xadmin.site.register(Configuration, ConfigurationAdmin)

#####################################################################################
# 校勘任务

#
# class PauseSelectedTasksAction(BaseActionView):
#
#     action_name = "pause_selected_tasks"
#     description = '暂停所选的 任务'
#     icon = 'fa fa-pause'
#
#     @filter_hook
#     def do_action(self, queryset):
#         allowed_status = [Task.STATUS_READY, Task.STATUS_PROCESSING]
#         n = queryset.filter(status__in=allowed_status).update(
#             status=Task.STATUS_PAUSED)
#         if n:
#             self.message_user("成功暂停了%(count)d个任务。" % {
#                 "count": n,
#             }, 'success')
#
#
# class ContinueSelectedTasksAction(BaseActionView):
#
#     action_name = "continue_selected_tasks"
#     description = '继续所选的 任务'
#     icon = 'fa fa-play'
#
#     @filter_hook
#     def do_action(self, queryset):
#         n1 = queryset.filter(status=Task.STATUS_PAUSED,
#                              picker=None).update(status=Task.STATUS_READY)
#         n2 = queryset.filter(status=Task.STATUS_PAUSED).exclude(
#             picker=None).update(status=Task.STATUS_PROCESSING)
#         if n1 or n2:
#             msg = "成功将%d个任务的状态变为待领取，将%d个任务的状态变为进行中。" % (n1, n2)
#             self.message_user(msg, 'success')
#
#
# class ReclaimSelectedTasksAction(BaseActionView):
#
#     action_name = "reclaim_selected_tasks"
#     description = '回收所选的 任务'
#     icon = 'fa fa-unlink'
#
#     @filter_hook
#     def do_action(self, queryset):
#         n = queryset.filter(status=Task.STATUS_PROCESSING).update(
#             status=Task.STATUS_READY, picker=None, picked_at=None)
#         if n:
#             msg = "成功将%d个任务的状态变为待领取。" % n
#             self.message_user(msg, 'success')
#
# class RemindSelectedTasksAction(BaseActionView):
#
#     action_name = "remind_selected_tasks"
#     description = '对所选的任务催单'
#     icon = 'fa fa-bell'
#
#     @filter_hook
#     def do_action(self, queryset):
#         n = queryset.filter(status=Task.STATUS_PROCESSING).update(
#             status=Task.STATUS_REMINDED)
#         if n:
#             self.message_user("成功对%(count)d个任务催单。" % {
#                 "count": n,
#             }, 'success')
#
# class SetPriorityActionBase(BaseActionView):
#     icon = 'fa fa-tasks'
#
#     @filter_hook
#     def do_action(self, queryset):
#         n = queryset.update(priority=self.priority)
#         if n:
#             self.message_user("成功将%(count)d个任务%(description)s。" % {
#                 "count": n,
#                 "description": self.description,
#             }, 'success')
#
#
# class SetHighPriorityAction(SetPriorityActionBase):
#     action_name = "set_high_priority"
#     description = '设为高优先级'
#     priority = 3
#
#
# class SetMiddlePriorityAction(SetPriorityActionBase):
#     action_name = "set_middle_priority"
#     description = '设为中优先级'
#     priority = 2
#
#
# class SetLowPriorityAction(SetPriorityActionBase):
#     action_name = "set_low_priority"
#     description = '设为低优先级'
#     priority = 1
#
#
# class UpdateTaskResultAction(BaseActionView):
#
#     action_name = "update_task_result"
#     description = '更新任务数据'
#     icon = 'fa fa-refresh'
#
#     @filter_hook
#     def do_action(self, queryset):
#         types = [Task.TYPE_CORRECT, Task.TYPE_CORRECT_VERIFY]
#         task_lst = list(queryset.filter(
#             typ__in=types, status=Task.STATUS_FINISHED))
#         for task in task_lst:
#             correct_update_async(task.id)
#         if task_lst:
#             self.message_user("成功对%(count)d个任务做了数据更新。" % {
#                 "count": len(task_lst),
#             }, 'success')
#
# class GeneTaskPlugin(BaseAdminPlugin):
#     gene_task = False
#     # Block Views
#     def block_top_toolbar(self, context, nodes):
#         if self.gene_task:
#             context.update({
#                 "title": '生成任务',
#             })
#             nodes.append(loader.render_to_string('tasks/gene_button.html',
#                                                  {
#                                                      "title": '生成任务',
#                                                  }))
#
# site.register_plugin(GeneTaskPlugin, ListAdminView)

# @xadmin.sites.register(Task)
# class TaskAdmin(object):
#     def modify(self, instance):
#         return '修改'
#     modify.short_description = '操作'
#
#     def task_link(self, instance):
#         if instance.status in [Task.STATUS_PROCESSING, Task.STATUS_PAUSED, Task.STATUS_FINISHED]:
#             return '<a target="_blank" href="/%s/%d/">查看</a>' % \
#             (Task.TYPE_TO_URL_PREFIX[instance.typ], instance.id)
#         else:
#             return ''
#     task_link.allow_tags = True
#     task_link.short_description = '查看任务'
#     list_display = ['batchtask', 'tripitaka_name', 'sutra_name', 'lqsutra_name', 'base_reel_name',
#                     'reel_no', 'typ', 'priority', 'task_no', 'realtime_progress', 'status',
#                     'publisher', 'created_at', 'picker', 'picked_at', 'finished_at', 'task_link', 'modify']
#     list_display_links = ("modify",)
#     list_filter = ['typ', 'batchtask', 'picker', 'status', 'task_no']
#     search_fields = ['reel__sutra__tripitaka__name', 'reel__sutra__tripitaka__code',
#                      'reel__sutra__name', '=reel__reel_no', 'lqreel__lqsutra__name']
#     fields = ['status', 'result', 'picked_at', 'picker', 'priority']
#     remove_permissions = ['add']
#     gene_task = True
#     actions = [PauseSelectedTasksAction, ContinueSelectedTasksAction,
#                ReclaimSelectedTasksAction, RemindSelectedTasksAction,
#                SetHighPriorityAction, SetMiddlePriorityAction, SetLowPriorityAction,
#                UpdateTaskResultAction]
#
# @xadmin.sites.register(JudgeFeedback)
# class JudgeFeedbackAdmin:
#     def task_link(self, instance):
#         return '<a target="_blank" href="/judgefeedback/%d/">查看</a>' % instance.id
#     task_link.allow_tags = True
#     task_link.short_description = '查看'
#     list_display = ['lqsutra_name', 'reel_no', 'fb_user', 'created_at',
#                     'fb_comment', 'processor', 'processed_at', 'response', 'task_link']
#     list_display_links = [''] # 不显示修改的链接
#     remove_permissions = ['add']
#
# @xadmin.sites.register(LQPunctFeedback)
# class LQPunctFeedbackAdmin:
#     def task_link(self, instance):
#         return '<a target="_blank" href="/lqpunctfeedback/%d/">查看</a>' % instance.id
#     task_link.allow_tags = True
#     task_link.short_description = '查看'
#     list_display = ['lqpunct', 'start', 'end', 'fb_punctuation',
#                     'fb_user', 'created_at', 'processor', 'processed_at',
#                     'status', 'task_link']
#     list_display_links = ['']  # 不显示修改的链接
#     remove_permissions = ['add']
#
# @xadmin.sites.register(AbnormalLineCountTask)
# class AbnormalLineCountTaskAdmin:
#     list_display = ['reel', 'reel_page_no', 'page_no', 'bar_no',
#                     'line_count', 'status', 'picker', 'picked_at', 'task_url']
#     list_editable = ['status']
#     list_display_links = ['']  # 不显示修改的链接
#     list_filter = ['status']
#     search_fields = ['reel__sutra__tripitaka__name', 'reel__sutra__tripitaka__code',
#                      'reel__sutra__name', '=reel__reel_no']
#     remove_permissions = ['add']

#####################################################################################
# 切分数据配置

#
# @xadmin.sites.register(Reel_Task_Statistical)
# class Reel_Task_StatisticalAdmin(object):
#     def resume_pptask(self, instance):
#         task_header = "%s_%s" % (
#             instance.schedule.schedule_no, instance.reel_id)
#         count = PageTask.objects.filter(
#             number__regex=r'^' + task_header + r'.*', status=TaskStatus.NOT_READY).count()
#         if count > 0:
#             return """<a class='btn btn-success' href='/xadmin/rect/reel_pptask/open/?schedule_no=%s&reel_id=%s&pk=%s'>%s</a>""" % (instance.schedule.schedule_no,  instance.reel_id, instance.pk,  u"打开逐字校对")
#         return '已打开'
#     resume_pptask.short_description = "打开逐字校对"
#     resume_pptask.allow_tags = True
#     resume_pptask.is_column = True
#
#     list_display = ('schedule', 'reel', 'amount_of_pptasks',
#                     'completed_pptasks', 'updated_at', )
#     list_display_links = ('completed_cctasks', 'reel')
#     search_fields = ('amount_of_cctasks', 'completed_cctasks')
#     list_filter = ('completed_cctasks',)
#
#
# # 1
# @xadmin.sites.register(Schedule)
# class ScheduleAdmin(object):
#     browser_details = {'name': {'title': u'置信度阀值预览', 'load_url': 'detail2'}}
#
#     def remain_task_count(self, instance):
#         count = CCTask.objects.filter(
#             schedule=instance.id, status__in=TaskStatus.remain_status).count()
#         if count > 0:
#             return """<a href='/xadmin/rect/cctask/?schedule_id__exact=%s'>%s</a>""" % (instance.id, count)
#         return count
#     remain_task_count.short_description = "未完置信任务数"
#     remain_task_count.allow_tags = True
#     remain_task_count.is_column = True
#
#     list_display = ("name", "cc_threshold", "status", "due_at",
#                     'created_at', 'remain_task_count')
#     list_display_links = ("name", )
#     list_filter = ('status', 'due_at', 'created_at')
#     search_fields = ["name"]
#     list_editable = ("cc_threshold",)
#     date_hierarchy = 'due_at'
#     relfield_style = "fk-select"
#     reversion_enable = True
#     style_fields = {'reels': 'm2m_transfer'}
#
# # 2目前不需要显示
# # @xadmin.sites.register(Schedule_Task_Statistical)
# # class Schedule_Task_StatisticalAdmin(object):
# #     list_display = ('schedule', 'amount_of_cctasks', 'completed_cctasks', 'amount_of_classifytasks',
# #         'completed_classifytasks', 'amount_of_absenttasks', 'completed_absenttasks', 'amount_of_pptasks',
# #         'completed_pptasks', 'amount_of_vdeltasks', 'completed_vdeltasks', 'amount_of_reviewtasks',
# #         'completed_reviewtasks', 'remark', 'updated_at')
# #     list_display_links = ('completed_cctasks',)
# #     search_fields = ('amount_of_cctasks',)
# #     list_editable = ('remark',)
# #     list_filter = ('completed_cctasks',)
#
# # 3
#
#
# @xadmin.sites.register(CCTask)
# class CCTaskAdmin(object):
#     list_display = ("number", "schedule", "ttype", "status",
#                     "update_date", "rect_set", "owner")
#     list_display_links = ("number",)
#     list_filter = ("number", 'update_date')
#     search_fields = ["owner__email", "status"]
#     list_editable = ('owner', "status")
#     date_hierarchy = 'update_date'  # 详细时间分层筛选
#     relfield_style = "fk-select"
#
#
# @xadmin.sites.register(CharClassifyPlan)
# class CharClassifyPlanAdmin(object):
#
#     browser_details = {'ch': {'title': u'聚类字块详情页', 'load_url': 'detail2'}}
#
#     list_display = ("schedule", "ch", "total_cnt",
#                     "needcheck_cnt", "wcc_threshold", )
#     list_display_links = ("total_cnt",)
#     list_filter = ("ch", 'total_cnt')
#     search_fields = ["ch", "total_cnt"]
#     list_editable = ('wcc_threshold',)
#     date_hierarchy = 'wcc_threshold'  # 详细时间分层筛选
#     relfield_style = "fk-select"
#
#
# @xadmin.sites.register(ClassifyTask)
# class ClassifyTaskAdmin(object):
#     list_display = ("number", "schedule", "ttype", "status",
#                     "update_date", "rect_set", "owner")
#     list_display_links = ("number",)
#     list_filter = ("number", 'update_date')
#     search_fields = ["owner__email", "status"]
#     list_editable = ('owner', "status")
#     date_hierarchy = 'update_date'  # 详细时间分层筛选
#     relfield_style = "fk-select"
#
#
# @xadmin.sites.register(DelTask)
# class DelTaskAdmin(object):
#     list_display = ("number", "schedule", "ttype", "status",
#                     "update_date", "rect_set", "owner")
#     list_display_links = ("number",)
#     list_filter = ("number", 'update_date')
#     search_fields = ["owner__email", "status"]
#     list_editable = ('owner', "status")
#     date_hierarchy = 'update_date'  # 详细时间分层筛选
#     relfield_style = "fk-select"
#
#
# @xadmin.sites.register(PageTask)
# class PageTaskAdmin(object):
#     list_display = ("number", "schedule", "ttype", "status",
#                     "update_date", "page_set", "owner")
#     list_display_links = ("number",)
#     list_filter = ("number", 'update_date')
#     search_fields = ["owner__email", "status"]
#     list_editable = ('owner', "status")
#     date_hierarchy = 'update_date'  # 详细时间分层筛选
#     relfield_style = "fk-select"
#
#
# @xadmin.sites.register(AbsentTask)
# class AbsentTaskAdmin(object):
#     list_display = ("number", "schedule", "ttype", "status",
#                     "update_date", "page_set", "owner")
#     list_display_links = ("number",)
#     list_filter = ("number", 'update_date')
#     search_fields = ["owner__email", "status"]
#     list_editable = ('owner', "status")
#     date_hierarchy = 'update_date'  # 详细时间分层筛选
#     relfield_style = "fk-select"
#
#
#
# @xadmin.sites.register(BatchTask)
# class BatchTaskAdmin(object):
#     list_display = ("id",
#                     "batch_no",
#                     "dataRange","priority",
#                     "CORRECT_finished","CORRECT_VERIFY_finished",
#                     "JUDGE_finished","JUDGE_VERIFY_finished",
#                     "PUNCT_finished","PUNCT_VERIFY_finished",
#                     "MARK_finished","MARK_VERIFY_finished",
#                     "publisher",
#                     "created_at",
#                      )
#     list_display_links = ("id")
#     list_filter = ( "publisher", )
#     #search_fields = [ "created_at"]
#     #list_editable = ("priority",)
#     #date_hierarchy = 'created_at'  # 详细时间分层筛选
#     relfield_style = "fk-select"
#     fields = ('priority',)
#
#     actions = [SetHighPriorityAction, SetMiddlePriorityAction, SetLowPriorityAction,]
#
#     def __any_finished(self,obj,typ):
#         FINISHED_count =  len( Task.objects.filter( batchtask= obj   , typ=typ,status=4) )
#         ALL_count =  len( Task.objects.filter( batchtask= obj   , typ=typ))
#         strRet=""
#         if ( ALL_count !=0 ):
#             strRet='%d/%d(%d%%)'%(FINISHED_count,ALL_count,int(100*FINISHED_count/ALL_count))
#         return strRet
#
#     #文字校对任务完成情况
#     def CORRECT_finished(self, obj):
#         return self.__any_finished(obj,1)
#
#     CORRECT_finished.short_description = u'文字校对进度'
#     CORRECT_finished.allow_tags = True
#
#     #文字校对任务完成情况
#     def CORRECT_VERIFY_finished(self, obj):
#         return self.__any_finished(obj,2)
#
#     CORRECT_VERIFY_finished.short_description = u'文字校对审定进度'
#     CORRECT_VERIFY_finished.allow_tags = True
#     #校勘判取任务完成情况
#     def JUDGE_finished(self, obj):
#         return self.__any_finished(obj,3)
#
#     JUDGE_finished.short_description = u'校勘判取进度'
#     JUDGE_finished.allow_tags = True
#
#     #校勘审定任务完成情况
#     def JUDGE_VERIFY_finished(self, obj):
#         return self.__any_finished(obj,4)
#
#     JUDGE_VERIFY_finished.short_description = u'校勘审定进度'
#     JUDGE_VERIFY_finished.allow_tags = True
#
#     #标点任务完成情况
#     def PUNCT_finished(self, obj):
#         return self.__any_finished(obj,5)
#
#     PUNCT_finished.short_description = u'标点进度'
#     PUNCT_finished.allow_tags = True
#
#     #标点任务完成情况
#     def PUNCT_VERIFY_finished(self, obj):
#         return self.__any_finished(obj,6)
#
#     PUNCT_VERIFY_finished.short_description = u'标点审定进度'
#     PUNCT_VERIFY_finished.allow_tags = True
#
#     #格式标注任务完成情况
#     def MARK_finished(self, obj):
#         return self.__any_finished(obj,9)
#
#     MARK_finished.short_description = u'格式标注进度'
#     MARK_finished.allow_tags = True
#
#       #格式标注任务完成情况
#     def MARK_VERIFY_finished(self, obj):
#         return self.__any_finished(obj,10)
#
#     MARK_VERIFY_finished.short_description = u'格式标注审定进度'
#     MARK_VERIFY_finished.allow_tags = True
#
#     #按照校勘判取任务判断
#     def dataRange(self, obj):
#         mydataRange={}
#         t_tasks =  Task.objects.filter( batchtask= obj).order_by('reel','typ')#t_tasks =  Task.objects.filter( batchtask= obj , typ = 3 ,task_no=2  ).order_by('lqreel')
#         strRet=''
#         if len( t_tasks) >0 :
#             #构建去重复数据的数组
#             for t in t_tasks:
#                 if t and t.reel and t.reel.sutra :
#                     reel_no=t.reel.reel_no
#                     if ( mydataRange.get(t.reel.sutra.name) == None ):#新经
#                         newPageDict={}
#                         mydataRange[t.reel.sutra.name] = newPageDict#初始化
#                     curPageDict=mydataRange[t.reel.sutra.name]
#                     curPageDict[reel_no]=reel_no
#             strRet=''
#
#             #循环判断
#             for key in mydataRange :
#                 curPageDict=mydataRange[key]
#                 index = -1
#                 indexBegin = -1
#                 n = len(curPageDict) - 1
#                 i=0
#                 for subkey in curPageDict:#
#                     if (subkey - index != 1 ) : #不连续
#                         if ( index != indexBegin ):
#                             strRet += "-"+str(index) #先把前面连续的输出了
#                         if (i == 0):
#                             strRet += key + "("+str(subkey)
#                         else:
#                             strRet += "/"+str(subkey)
#                         indexBegin = subkey
#                     if ( i == n ):
#                         if ( subkey -index == 1):
#                             strRet += "-"+str(subkey)
#                         strRet += ")"
#                     index=subkey
#                     i+=1
#         return strRet
#     #end   dataRange
#
#     dataRange.short_description = u'数据范围'
#     dataRange.allow_tags = True
#
#     def batch_no(self, obj):
#         return '%d%02d%02d%02d%02d' % (obj.created_at.year,
#                 obj.created_at.month, obj.created_at.day, obj.created_at.hour,
#                 obj.created_at.minute)
#
#     batch_no.short_description = u'批次号'
#     batch_no.allow_tags = True
#


    

    
# @xadmin.sites.register(Permission)
# class PermissionAdmin(object):
#     list_display = ('id', 'name', 'menu', 'get_roles', 'is_active')
#     fields = ('is_active', 'roles', 'menu')

#     def get_roles(self, obj):
#         return ",".join([r.name for r in obj.roles.all()])

# @xadmin.sites.register(Resource)
# class ResourceAdmin(object):
#     pass

# @xadmin.sites.register(Role)
# class RoleAdmin(object):
#     list_display = ('id', 'name')


# @xadmin.sites.register(Menu)
# class MenuAdmin(object):
#     list_display = ('id', 'name', 'menu_paths', 'is_active')
#     fields = ('menu_paths', 'is_active' )


#####################################################################################

#
# class GlobalSetting(object):
#     site_title = '龙泉大藏经'  # 设置头标题
#     site_footer = '北京 龙泉寺-AIITC.inc'  # 设置脚标题
#
#     def rect_data_menu(self):
#         return [{
#                 # 'perm': self.get_model_perm(Reel_Task_Statistical, 'view'),
#                 'title': u'藏经切分管理',
#                 'icon': 'fa fa-cut',
#                 'menus': (
#                     {'title': u'总体进度', 'url': self.get_model_url(
#                         Reel_Task_Statistical, 'changelist'), 'icon': 'fa fa-tasks', },
#                     {'title': u'切分计划',  'url': self.get_model_url(
#                         Schedule, 'changelist'), 'icon': 'fa fa-calendar', },
#                     {'title': u'置信校对',  'url': self.get_model_url(
#                         CCTask, 'changelist'), 'icon': 'fa fa-edit', },
#                     {'title': u'聚类校对',  'url': self.get_model_url(
#                         ClassifyTask, 'changelist'), 'icon': 'fa fa-edit', },
#                     {'title': u'查漏校对',  'url': self.get_model_url(
#                         AbsentTask, 'changelist'), 'icon': 'fa fa-edit', },
#                     {'title': u'逐字校对',  'url': self.get_model_url(
#                         PageTask, 'changelist'), 'icon': 'fa fa-edit', },
#                     {'title': u'删框审定',  'url': self.get_model_url(
#                         DelTask, 'changelist'), 'icon': 'fa fa-stethoscope', },
#                     {'title': u'反馈检查',   'icon': 'fa fa-ban', },
#                     {'title': u'聚类阈值',  'url': self.get_model_url(
#                         CharClassifyPlan, 'changelist'),   'icon': 'fa fa-circle'},
#                 )}, ]
#
#     def data_mana_menu(self):
#         return [{
#                 'title': u'藏经数据管理',
#                 'icon': 'fa fa-cloud',
#                 'menus': (
#                     {'title': u'龙泉经目', 'url': self.get_model_url(
#                         LQSutra, 'changelist'), 'icon': 'fa fa-book', },
#                     {'title': u'实体藏',  'url': self.get_model_url(
#                         Tripitaka, 'changelist'), 'icon': 'fa fa-book', },
#                     {'title': u'实体册',  'url': self.get_model_url(
#                         Volume, 'changelist'), 'icon': 'fa fa-book', },
#                     {'title': u'实体经',  'url': self.get_model_url(
#                         Sutra, 'changelist'), 'icon': 'fa fa-book', },
#                     {'title': u'实体卷',  'url': self.get_model_url(
#                         Reel, 'changelist'), 'icon': 'fa fa-book', },
#                     {'title': u'配置',  'url': self.get_model_url(
#                         Configuration, 'changelist'), 'icon': 'fa fa-cog', },
#                 )}, ]
#
#     def user_mana_menu(self):
#         return [{
#                 # 'perm': self.get_model_perm(LQSutra, 'view'),
#                 'title': u'用户中心',
#                 'icon': 'fa fa-book',
#                 'menus': (
#                     {'title': u'用户维护', 'url': self.get_model_url(
#                         Staff, 'changelist'), 'icon': 'fa fa-book', },
#                     # {'title': u'角色维护', 'url': self.get_model_url(Role, 'changelist'),'icon':'fa fa-book',},
#                     # {'title': u'菜单管理', 'url': self.get_model_url(Menu, 'changelist'),'icon':'fa fa-book',},
#                     # {'title': u'权限管理', 'url': self.get_model_url(Permission, 'changelist'),'icon':'fa fa-book',},
#                 )}, ]
#
#     def get_site_menu(self):
#         menus = []
#         menus.extend(self.rect_data_menu())
#         menus.extend(self.data_mana_menu())
#         menus.extend(self.user_mana_menu())
#         return menus
#
#     menu_style = 'accordion'


#xadmin.site.register(views.CommAdminView, GlobalSetting)

#####################################################################################

from django.contrib import admin
from .models import Candidate
from django.http import HttpResponse
import csv
from datetime import datetime
from interview import candidate_field as cf
import logging

logger = logging.getLogger(__name__)

exportable_fields = ('username', 'city', 'phone', 'bachelor_school', 'master_school', 'degree', 'first_result',
                     'first_interviewer_user','second_result', 'second_interviewer_user', 'hr_result', 'hr_score',
                     'hr_remark', 'hr_interviewer_user')


#导出csv文件
def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachment; filename=%s-list-%s.csv' % (
        'recruitment-candidates',
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )
    # 写入表头
    writer = csv.writer(response)
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list],
    )
    for obj in queryset:
        ## 单行 的记录（各个字段的值）， 根据字段对象，从当前实例 (obj) 中获取字段值
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)

    logger.error(" %s has exported %s candidate records" % (request.user.username, len(queryset)))
    return response


export_model_as_csv.short_description = u'导出为CSV文件'


class CandidateAdmin(admin.ModelAdmin):
    #生成到处的action
    actions = (export_model_as_csv,)
    #新生成的时候排除的字段
    exclude = ('creator', 'created_date', 'modified_date')
    #显示的字段
    list_display = (
        'username', 'city', 'bachelor_school', 'first_score', 'first_result', 'first_interviewer_user',
        'second_result', 'second_interviewer_user', 'hr_score', 'hr_result', 'hr_interviewer_user',
        'last_editor',)
    #待搜索的字段
    search_fields = ('username', 'phone', 'email', 'bachelor_school')
    #右侧筛选
    list_filter = ('city','first_result','second_result','hr_result','first_interviewer_user',
                   'second_interviewer_user','hr_interviewer_user')
    #默认排序
    ordering = ('hr_result', 'second_result', 'first_result',)

    def get_list_editable(self, request):
        group_names = self.get_group_names(request.user)

        if request.user.is_superuser or 'hr' in group_names:
            return ('first_interviewer_user', 'second_interviewer_user',)
        return ()

    def get_changelist_instance(self, request):
        """
        override admin method and list_editable property value
        with values returned by our custom method implementation.
        """
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin, self).get_changelist_instance(request)

    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names

    def get_readonly_fields(self, request, obj):
        group_names = self.get_group_names(request.user)
        if 'interviewer' in group_names:
            logger.info("interviewer is in user's group for %s" % request.user.username)
            return ('first_interviewer_user', 'second_interviewer_user',)
        return ()

admin.site.register(Candidate, CandidateAdmin)
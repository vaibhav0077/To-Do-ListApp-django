import django_tables2 as tables
from .models import TODO
from django_tables2.utils import A
import datetime


def status_decision(**kwargs):
    row = kwargs.get("record")
    d1 = datetime.datetime.today()
    today_date = d1.date()
    # print((row.end_date - today_date).days)
    if row.status == 'C':
        return "color:green; "
    else:
        if(row.end_date - today_date).days <= 3 and (row.end_date - today_date).days > 0:
             return "color:blue;"
        elif (row.end_date - today_date).days > 3:
            return "color:black;"
        else:
            return "color:red;"


class TODOTable(tables.Table):
    id = tables.Column(verbose_name='Task Id')
    delete = tables.TemplateColumn(
        template_name='base/task_delete_btn.html', orderable=False)
    edit = tables.TemplateColumn(
        template_name='base/task_edit_btn.html', orderable=False)

    title = tables.LinkColumn('view_todo', args=[A('id')])


    class Meta:
        row_attrs = {
            "style": status_decision
        }   
        model = TODO
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ("id", "title", "status", "date",
                  "priority", "end_date", "edit", "delete")
        labels = {'end_date': 'End-date'}

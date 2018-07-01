from django.core.management.base import BaseCommand, CommandError
from segment.models import PageRect, PageRectStatus, ColumnRect


class Command(BaseCommand):
    def handle(self, *args, **options):
        toCutColumnList = PageRect.objects.filter(status=PageRectStatus.CUT_PAGE_COMPLETED)
        columns = []
        for pagerect in toCutColumnList:
            # todo 执行切列的算法.
            array = []
            clno, x, y, w, h = array
            column = ColumnRect.create_columnRect(pagerect, clno, x, y, w, h)
            if column: columns.append(column)
        PageRect.objects.bulk_create(columns)


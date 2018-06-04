from django.core.management.base import BaseCommand
from django.conf import settings
from tdata.models import Tripitaka


class Command(BaseCommand):
    def handle(self, *args, **options):
        filename = '%s/data/tripitaka_list.txt' % settings.BASE_DIR
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                code, name, shortname = line.rstrip().split()
                tripitaka = Tripitaka(code=code, name=name, shortname=shortname)
                tripitaka.save()
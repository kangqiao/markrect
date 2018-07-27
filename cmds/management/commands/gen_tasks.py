from django.core.management.base import BaseCommand, CommandError
from bulk_update.helper import bulk_update
from django.conf import settings
from tdata.models import *
from segment.models import *
from segment.gen_tasks import *
import random


class Command(BaseCommand):
    def handle(self, *args, **options):
        test_gen_pagerect_test_data()
        gen_pagerect_task()

        test_gen_column_task()
        gen_column_task()

        test_gen_char_task()
        gen_char_task()



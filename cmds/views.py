from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings

from tdata.models import *
from tdata.lib.image_name_encipher import get_image_url

def cutfixed_pages(request):
    queryset = Page.objects.exclude(cut_updated_at__isnull=True).values_list('pid', 'cut_updated_at', named=True)
    page_list = [{
        'pid': r.pid,
        'cut_updated_at': int(r.cut_updated_at.timestamp())
        } for r in queryset]
    return render(request, 'cmds/cutfixed_pages.html', {'page_list': page_list})

def cutfixed_page_detail(request, pid):
    page = get_object_or_404(Page, pid=pid)
    image_url = get_image_url(page.reel, page.page_no)
    return render(request, 'cmds/cutfixed_page_detail.html', {'page': page, 'image_url': image_url})
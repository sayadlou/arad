import os
from datetime import datetime, timedelta
from time import mktime

import requests
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from .models import Post as LearningPost, VideoFile
from .permitions import BoughtUserMixin
from django_downloadview import ObjectDownloadView

from ..store.forms import CartItemForm


class IndexView(ListView):
    model = LearningPost
    template_name = 'learning/index.html'
    paginate_by = 6

    # all_posts = Post.objects.order_by('pub_date').filter(status='Published')

    def get_queryset(self):
        return self.model.objects.order_by('pub_date').filter(status='Published')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['model'] = ContentType.objects.get_for_model(LearningPost).pk
        data['formmy'] = CartItemForm()

        return data


class SlugView(BoughtUserMixin, DetailView):
    template_name = 'learning/slug.html'
    model = LearningPost

    def get_context_data(self, **kwargs):
        validity_link_time = datetime.now() + timedelta(hours=10)
        validity_link_time_unix = int(mktime(validity_link_time.timetuple()))
        url = f"https://napi.arvancloud.com/vod/2.0/videos/{self.object.video.arvan_id}"
        headers = {'Authorization': os.environ.get('arvan_api_key')}
        payload = {'secure_expire_time': validity_link_time_unix, 'secure_ip': '1.1.1.1'}
        if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production':
            payload['secure_ip'] = self.get_client_ip()
        r = requests.get(url, headers=headers)
        data = super().get_context_data(**kwargs)
        if r.status_code == 200:
            respone = r.json()
            data['video_url'] = respone["data"]["player_url"]
            data['status'] = True
        else:
            data['status'] = False
        return data

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class TagView(ListView):
    model = LearningPost
    template_name = 'learning/tag.html'
    paginate_by = 6

    def get_queryset(self):
        tag = self.request.GET.get("tag", "")
        tag = tag.lower()
        return self.model.objects.order_by('pub_date').filter(status='Published').filter(tags__contains=[tag])


class CategoryView(ListView):
    model = LearningPost
    template_name = 'learning/category.html'
    paginate_by = 6

    def get_queryset(self):
        category = self.kwargs['category']
        return self.model.objects.order_by('pub_date').filter(category__name__iexact=category)


class AttachmentView(BoughtUserMixin, ObjectDownloadView):
    model = LearningPost
    file_field = "attachment"


@staff_member_required
def refresh(request):
    url = f"https://napi.arvancloud.com/vod/2.0/channels/{os.environ.get('arvan_channel_id')}/videos"
    headers = {'Authorization': os.environ.get('arvan_api_key')}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        respone = r.json()
        ids = VideoFile.objects.values_list('arvan_id')
        list(ids)
        id_list = [i[0] for i in ids]
        video_file = []
        for video in respone['data']:
            if video['id'] not in id_list:
                video_file.append(VideoFile(arvan_id=video['id'], name=video['title']))
        VideoFile.objects.bulk_create(video_file)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

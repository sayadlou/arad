from azbankgateways.urls import az_bank_gateways_urls
from django.conf.urls import url
from django.urls import path, include


urlpatterns = [
    path('', include(('apps.core.urls', 'apps.core'), namespace='core')),
    path('', include(('apps.store.urls', 'apps.store'), namespace='store')),
    path('account/', include(('apps.account.urls', 'apps.account'), namespace='account')),
    path('blog/', include(('apps.blog.urls', 'apps.blog'), namespace='blog')),
    path('captcha/', include('captcha.urls')),
    path('contact_us/', include(('apps.contact_us.urls', 'apps.contact_us'), namespace='contact_us')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('bankgateways/', az_bank_gateways_urls()),
    url(r'^filer/', include('filer.urls')),
]



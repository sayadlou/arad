from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.account.forms import AuthAdminForm
from .base import urlpatterns
from ..settings.base import MEDIA_URL, MEDIA_ROOT, STATIC_URL, STATIC_ROOT


admin.autodiscover()
admin.site.login_form = AuthAdminForm
admin.site.login_template = 'admin/login.html'

urlpatterns += [
    path('site_manager/', admin.site.urls),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),

]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)

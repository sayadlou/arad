import debug_toolbar
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from .base import urlpatterns
# from apps.core.admin import AuthAdminForm

from ..settings.base import MEDIA_URL, MEDIA_ROOT, STATIC_URL, STATIC_ROOT

# admin.autodiscover()
# admin.site.login_form = AuthAdminForm
# admin.site.login_template = 'admin/login.html'

urlpatterns += [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),

]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)


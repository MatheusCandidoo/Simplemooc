from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

app_name = 'home'

urlpatterns = [
    path('', include('simplemooc.core.urls'),),
    path('conta/', include('simplemooc.accounts.urls',)),
    path('cursos/', include('simplemooc.courses.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

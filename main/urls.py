from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from users.views import login


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name='login'),
    path('user/', include('users.urls', namespace='user')),
    path('finances/', include('finances.urls', namespace='finances')),
    path('pdf_gen/', include('pdf_gen.urls', namespace='pdf_gen')),
    path('investing/', include('investing.urls', namespace='investing')),
    path('budgets/', include('budgets.urls', namespace='budgets'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

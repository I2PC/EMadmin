from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import profiles.urls
import accounts.urls
import create_proj.urls
import create_report.urls
from . import views
import create_stat.urls
import invoice.urls

urlpatterns = [
    url(r'^$', views.HomePage.as_view(), name='home'),
    url(r'^about/$', views.AboutPage.as_view(), name='about'),
    url(r'^users/', include(profiles.urls, namespace='profiles')),
    url(r'^create_proj/', include(create_proj.urls, namespace='create_proj')),
    url(r'^create_stat/', include(create_stat.urls, namespace='create_stat')),
    url(r'^create_report/', include(create_report.urls, namespace='create_report')),
    url(r'^invoice/', include(invoice.urls, namespace='invoice')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(accounts.urls, namespace='accounts')),
]

# User-uploaded files like profile pics need to be served in development
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

# Include django debug toolbar if DEBUG is on
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

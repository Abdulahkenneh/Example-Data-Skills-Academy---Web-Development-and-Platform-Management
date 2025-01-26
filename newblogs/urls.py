from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from blogs.sitemaps import PostSitemap
from blogs import views
sitemaps = {
    "post": PostSitemap,
}

urlpatterns = [
    path('liberia/', admin.site.urls),
    path("",include('blogs.urls',namespace='blogs')),
    path("python-ide/",include('pythonIDE.urls',namespace='python-ide')),
    path('markitup/', include('markitup.urls')),
    path('logusers/',include('logusers.urls',namespace='logusers')),  
    path('summernote/', include('django_summernote.urls')), 
    # path('courses/', views.course_list, name='course_list'),
    path('quiz/', include(('quiz.urls','quiz'),namespace='quiz')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

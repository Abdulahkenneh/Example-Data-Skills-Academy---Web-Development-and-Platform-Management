from django.urls import path
from .views import ide_view,home,access_code_view,user_access_code_view
from django.conf import settings
from django.conf.urls.static import static


app_name='python-ide'

urlpatterns =[
     path('',ide_view,name='ide'),
     path('home',home,name='home'),
     path('access_code/', access_code_view, name='access_code'),
      path('user_access_code/<int:course_id>/', user_access_code_view, name='user_access_code'),
     
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

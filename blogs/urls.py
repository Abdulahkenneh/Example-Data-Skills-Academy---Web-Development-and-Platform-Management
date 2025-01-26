from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.static import serve
from django.views.generic.base import TemplateView
from .sitemaps import PostSitemap, CourseTopicSitemap,CourseSitemap  # Import your sitemap classes
from .views import (
    home, recent_posts, course_topics, mark_topic_complete,
    register_course, all_courses, profile, course_delete_confirmation_view,
    unregister_course, my_courses, motivation_view,
     quiz_results, take_quiz, add_course_topic, blogs_view,
    topics_view, download_achievement_view, share_achievement_view,
    create_blogpost, items_view,pofolio,post_detail_view,about,terms_of_service,
    abdulahcustomerdocument_view,discusionForumPost_view,discusion_forum_home,new_discusion_topic,discusion_topic_detail,
new_discusion_post,new_discusion_comment, multi_model_search_view,new_discusion_rating,apply_for_course,sucess_view,course_questions_view)

sitemaps = {
    'posts': PostSitemap,
    'topics': CourseTopicSitemap,
    'all_courses': CourseSitemap,
}

urlpatterns = [
    path('', home, name='home'),
    path('mycustomers/',abdulahcustomerdocument_view , name='mycustomers'),
    path('terms',terms_of_service,name='terms'),
    path('about/', about, name='about'),
    path('post/', blogs_view, name='post'),
    path('items/', items_view, name='items'),
    path('recent-posts/', recent_posts, name='recent_posts'),
    path('user-pofolio/<int:post_id>/',pofolio,name='user-pofolio'),
    path('add-topic/', add_course_topic, name='add_topic'),
    path('profile/', profile, name='profile'),
    path('achievements/download/<int:id>/', download_achievement_view, name='download_achievement'),
    path('achievements/share/<int:id>/', share_achievement_view, name='share_achievement'),
    path('all_courses/', all_courses, name='all_courses'),
    path('my_courses/', my_courses, name='my_courses'),
    path('registers/<int:course_id>/', register_course, name='register_course'),
    path('topics/<int:topic_id>/', topics_view, name='topics'),
    path('motivation/<int:course_id>/', motivation_view, name='motivation'),
    path('course-topics/<int:course_id>/', course_topics, name='course_topics'),
    path('course-topics-complete/complete/<int:topic_id>/', mark_topic_complete, name='mark_topic_complete'),
    path('unregister-course/<int:course_id>/', unregister_course, name='unregister_course'),
    path('confirm/<int:course_id>/', course_delete_confirmation_view, name='confirm'),
    path('course/<int:course_id>/quiz/', take_quiz, name='take_quiz'),
    path('course/<int:course_id>/quiz/results/', quiz_results, name='quiz_results'),
    path('entry/', create_blogpost, name='entry'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt/',TemplateView.as_view(template_name = 'blogs/robots.txt',content_type= 'text/plain')),
    path('post-detail/<int:post_id>/', post_detail_view, name='post-detail'),
    path('ads.txt', serve, {'path': 'ads.txt','document_root': settings.STATIC_ROOT,}),
    path('apply/', apply_for_course, name='apply_for_course'),
    path('sucess/', sucess_view, name='sucess'),
    path('course/<int:course_id>/topic/<int:topic_id>/questions/', course_questions_view, name='course_questions'),
    path('discusion-forum/<int:post_pk>/', discusionForumPost_view, name='discusion_forum_post_view'),
    path('discusion-forum-home/<int:course_pk>/',discusion_forum_home, name='discusion_forum_home'),
    path('discusion-topic/<int:pk>/', discusion_topic_detail, name='discusion_topic_detail'),
    path('new_discusion_topic/', new_discusion_topic, name='new_discusion_topic'),
    path('discusion-post/<int:pk>/new/', new_discusion_post, name='new_discusion_post'),
    path('discusion-post-comment/<int:post_pk>/comment/new/', new_discusion_comment, name='new_discusion_comment'),
    path('rate-post/<int:post_pk>/rate/', new_discusion_rating, name='new_discusion_rating'),
    path('search/', multi_model_search_view, name='search'),


]

# Include the following if statement for serving media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = 'blogs'

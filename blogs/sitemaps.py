from django.contrib.sitemaps import Sitemap
from .models import Post,CourseTopic,Course
from django.urls import reverse


class PostSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.created_at  # Assuming you have an 'updated_at' field in your Post model

class CourseTopicSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return CourseTopic.objects.all()

    def lastmod(self, obj):
        return obj.date

    def location(self, obj):
        return  reverse('blogs:topics', kwargs={'topic_id': obj.id})





class CourseSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Course.objects.all()
 # Assuming you have an 'updated_at' field in your Post model

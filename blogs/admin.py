# your_app/admin.py
from django.contrib import admin
from .models import LoginActivity
from .models import (Profile, Course,Post, CourseTopic,Achievement,
                     UserCourseTopicProgress,Question,UserAnswer,
                     Choice,Comment,ContactUs,Subcribe,NewSubscribers,Items,AbdulahCustomerDocument,ForumTopic,
                     ForumPost,DiscusionForum,Rating,PostComment,ForumTopic,Application
                     )

from django_summernote.admin import SummernoteModelAdmin


@admin.register(AbdulahCustomerDocument)
class AbdulahCustomerDocumentAdmin(admin.ModelAdmin):
    list_display = ['email','name','image','description']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']

@admin.register(NewSubscribers)
class NewSubcribersAdmin(admin.ModelAdmin):
    list_display = ['email']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'user']

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)


@admin.register(UserCourseTopicProgress)
class UserCourseTopicProgressAdmin(admin.ModelAdmin):
    list_display = ['user','topic','progress']


@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ['owner','title', 'price','discription']


@admin.register(CourseTopic)
class CourseTopicAdmin(SummernoteModelAdmin):
    summernote_fields = ('body',)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'certificate']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text']

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'text']


@admin.register(UserAnswer)
class UserCourseTopicAdmin(admin.ModelAdmin):
    list_display = ['question', 'user','choice']


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message']


@admin.register(Subcribe)
class SubcribeAdmin(admin.ModelAdmin):
    list_display = ['email']


@admin.register(Comment)
class ConmmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'message']





@admin.register(ForumTopic)
class ForumTopicAdmin(SummernoteModelAdmin):
    summernote_fields = ('title','description','message',)


@admin.register(DiscusionForum)
class DiscusionForumAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(PostComment)
class PostConmmentAdmin(SummernoteModelAdmin):
    summernote_fields = ('message',)



@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['rating']


@admin.register(ForumPost)
class ForumPostAdmin(SummernoteModelAdmin):
    summernote_fields = ('message',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'course']



@admin.register(LoginActivity)
class LoginActivityAdmin(admin.ModelAdmin):
    list_display = ('user','email','login_time', 'ip_address',)
    search_fields = ('user__username', 'ip_address')

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import uuid
from django.db.models.signals import pre_save
from django.dispatch import receiver
import os
from django.utils import timezone

class AbdulahCustomerDocument(models.Model):
    name = models.CharField(max_length=300,blank=False)
    email = models.EmailField()
    image = models.ImageField(upload_to='images/AbdulahImg',blank=True)
    description = models.TextField(blank=False,help_text='What do have have to say about this documents',verbose_name='Document Discription')


class Course(models.Model):
    image = models.ImageField(upload_to='images', height_field=None, width_field=None, blank=True)
    type = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    access = models.BooleanField(default=True)
    date = models.DateTimeField(default=timezone.now,null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_courses')
    registered_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='registered_courses', blank=True)

    def __str__(self):
        return self.title

    def is_complete(self, user):
        return all(
            UserCourseTopicProgress.objects.filter(user=user, topic=topic).first().completed
            for topic in self.coursetopic_set.all()
        )

    def overall_progress(self, user):
        topics = self.coursetopic_set.all()
        if not topics:
            return 0
        user_progress = UserCourseTopicProgress.objects.filter(user=user, topic__course=self)
        if not user_progress:
            return 0
        total_progress = sum(up.progress for up in user_progress)
        return total_progress / topics.count()

    def get_absolute_url(self):
        return reverse('blogs:all_courses')



class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post')
    title = models.CharField(max_length=200)
    description = models.TextField()
    body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    thumbnail = models.ImageField(upload_to='images', blank=True, null=True )



    def get_absolute_url(self):
        return reverse('blogs:post')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)



class CourseTopic(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images', height_field=None, width_field=None, blank=True)
    progress = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    ide = models.BooleanField(default=False,help_text='When check the code ide with display')

    def get_absolute_url(self):
        return f'/topics/{self.id}'

    def save(self, *args, **kwargs):
        # Generate a unique slug if it is not set
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while CourseTopic.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title




class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='images', height_field=None, width_field=None, blank=True)
    bio = models.TextField(blank=True)
    enroll_courses = models.ManyToManyField('Course', related_name='students', blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    proffections = models.CharField(max_length=200, blank=True)
    skills = models.CharField(max_length=300, blank=True)
    access_code = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.access_code:
            self.access_code = self.generate_unique_access_code()
        super().save(*args, **kwargs)

    def generate_unique_access_code(self):
        access_code = uuid.uuid4().hex[:10].upper()
        while Profile.objects.filter(access_code=access_code).exists():
            access_code = uuid.uuid4().hex[:10].upper()
        return access_code

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(pre_save, sender=Profile)
def delete_old_profile_image(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_profile = Profile.objects.get(pk=instance.pk)
    except Profile.DoesNotExist:
        return False

    if old_profile.image and old_profile.image != instance.image:
        if os.path.isfile(old_profile.image.path):
            os.remove(old_profile.image.path)




class Achievement(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title =models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    certificate = models.ImageField(upload_to='images', height_field=None, width_field=None, blank=True)

    class Meta:
        unique_together = ('title', 'user')

    def __str__(self):
        return f'{self.user},obtained {self.title} certificate on{self.date}'




#compiler


class UserCourseTopicProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey(CourseTopic, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'topic')

    def __str__(self):
        return f"{self.user.username} - {self.topic.title}"



class Question(models.Model):
    text = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    topic = models.ForeignKey(CourseTopic, on_delete=models.CASCADE, related_name='topics')

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class UserAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')



class ContactUs(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=False)
    message = models.TextField(blank=True,null= True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} send you {self.message} on {self.date}'


class Subcribe(models.Model):
    email = models.EmailField(blank=False,null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email} has subcribe on {self.date}'


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200,blank=True,null=True)
    message = models.TextField(blank=False,null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.message}'


class NewSubscribers(models.Model):
    email = models.EmailField(blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email} subscrbe on {self.date}'


class Items(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,blank=True,null=True)
    image = models.ImageField(upload_to='images', height_field=None, width_field=None, blank=True)
    discription = models.TextField(blank=False,null=True)
    price = models.IntegerField(blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} the price is {self.price}'


class DiscusionForum(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class ForumTopic(models.Model):
    restrict = models.BooleanField(default=False)
    forum = models.ForeignKey(DiscusionForum, on_delete=models.CASCADE, related_name='topics')
    description = models.TextField()
    message = models.TextField()
    title = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ForumPost(models.Model):
    restrict = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, related_name='posts')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:50]

class PostComment(models.Model):
    post = models.ForeignKey(ForumPost, related_name='comments', on_delete=models.CASCADE,blank=True,null=True)
    message = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.message[:30]


class Rating(models.Model):
    post = models.ForeignKey(ForumPost, related_name='ratings', on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.rating} by {self.created_by}'


class Application(models.Model):
    EXPERIENCE_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    educational_background = models.TextField()
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES)
   # resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.full_name} applied for {self.course.name}'

# track user that are active
class LoginActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField()
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

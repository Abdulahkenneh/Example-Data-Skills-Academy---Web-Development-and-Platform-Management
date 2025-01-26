# your_app/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile,Achievement,Application
from .models import Question, Choice, UserAnswer,CourseTopic,Post,Comment,ForumTopic,ContactUs,Subcribe,NewSubscribers,AbdulahCustomerDocument,DiscusionForum,ForumPost,PostComment, Rating
from django.contrib.auth.forms import UserCreationForm
from django_summernote.widgets import SummernoteWidget


class AbdulahCustomerDocumentForm(forms.ModelForm):
    class Meta:
        model = AbdulahCustomerDocument
        fields= '__all__'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','firstname','lastname','proffections','skills','email','phone','bio','address']

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields= ['title','certificate']




class UserAnswerForm(forms.ModelForm):
    class Meta:
        model = UserAnswer
        fields = ['choice']

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['choice'].queryset = question.choices.all()


class CourseTopicForm(forms.ModelForm):
    class Meta:
        model = CourseTopic
        fields = ['title', 'body', 'image','course']
        widgets = {
            'body': SummernoteWidget(),
        }





class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','description', 'body', 'thumbnail']
        widgets = {
            'body': SummernoteWidget(),
        }


class AccessCodeForm(forms.Form):
    access_code = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Access Code'}))

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name','email','message']



class SubcribeForm(forms.ModelForm):
    class Meta:
        model = Subcribe
        fields =['email']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title','message']

class NewsubcribersForm(forms.ModelForm):
    class Meta:
        model = NewSubscribers
        fields = ['email']




class DiscusionForumForm(forms.ModelForm):
    class Meta:
        model = DiscusionForum
        fields = '__all__'


class NewTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': SummernoteWidget(),
        }


class NewPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['message']
        # widgets = {
        #     'message': forms.Textarea(attrs={'class': 'form-control'}),
        # }

        widgets = {
            'message': SummernoteWidget(),
        }

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['message']
        widgets = {
            'message': SummernoteWidget(),
        }

class NewRatingForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=10, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Rating
        fields = ['rating']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['full_name', 'email', 'phone_number', 'educational_background', 'experience_level', 'course', 'additional_info']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'educational_background': forms.Textarea(attrs={'placeholder': 'Educational Background'}),
            'experience_level': forms.Select(),
            'course': forms.Select(),
            'additional_info': forms.Textarea(attrs={'placeholder': 'Additional Information'}),
        }


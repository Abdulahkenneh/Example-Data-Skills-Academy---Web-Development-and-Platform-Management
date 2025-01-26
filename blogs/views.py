


# views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
import os
import markdown2
from django.http import Http404
from .models import CourseTopic,ForumPost,DiscusionForum,ForumTopic
import markdown2
from pygments.formatters.html import HtmlFormatter
from django.contrib.auth.models import AnonymousUser
from pygments.formatters import HtmlFormatter
from .models import (
    Post, Course, CourseTopic, Profile, Achievement,
    UserCourseTopicProgress, Question, Choice, UserAnswer, Comment, Items
)

from datetime import datetime
from .forms import (
    ProfileForm, CommentForm, ContactForm,
    RegistrationForm,AchievementForm, UserAnswerForm,
    CourseTopicForm, PostForm,AbdulahCustomerDocumentForm,DiscusionForumForm,NewPostForm,NewRatingForm,NewCommentForm,NewTopicForm,ApplicationForm
)


from django.db.models import Q
 # Import the necessary models
from django.utils import timezone  #

def terms_of_service(request):
    current_year = datetime.now().year
    return render(request,'blogs/terms_of_service.html',{'current_year':current_year})

def home(request):
    """Home view displaying all items, courses, and paginated posts."""
    items = Items.objects.all()
    courses = Course.objects.all()
    post_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    topics = CourseTopic.objects.all()
    cleancode='<p>How are you </p>'
    post_id = request.GET.get('post_id')

    if post_id:
        post = get_object_or_404(Post, id=post_id)
    else:
        post = page_obj.object_list[0] if page_obj.object_list else None

    contact_form = ContactForm(request.POST or None)

    if request.method == 'POST':
        if 'contact_submit' in request.POST and contact_form.is_valid():
            contact_form.save()
            return redirect('blogs:home')

    context = {
        'contact_form': contact_form,
        'courses': courses,
        'topics': topics,
        'page_obj': page_obj,
        'post': post,
        'items': items,
         'cleancode':cleancode
    }
    return render(request, 'blogs/home.html', context)



def about(request):
    return render(request, 'blogs/about.html')

def topics_view(request, topic_id):
    courses = Course.objects.all()
    """View to display a specific topic and highlight its code."""
    # Create a single HtmlFormatter instance
    formatter = HtmlFormatter(style='monokai')
    css_string = formatter.get_style_defs('.codehilite')

    # Fetch all topics and the specific topic by ID
    topics = CourseTopic.objects.all()
    topic = get_object_or_404(CourseTopic, id=topic_id)

    # Convert the topic body from Markdown to HTML with syntax highlighting
    topic.body = markdown2.markdown(topic.body, extras=["fenced-code-blocks", "code-friendly", "code-color"])

    # Prepare the context for rendering the template
    context = {
        'topic': topic,
        'topics': topics,
        'pygments_css': css_string,
        'courses':courses,
    }

    # Render the template with the provided context
    return render(request, 'blogs/topics.html', context)



def post_detail_view(request, post_id):
    posts = Post.objects.all().order_by('-created_at')
    post = get_object_or_404(Post, id=post_id)
    post.body = markdown2.markdown(post.body, extras=["fenced-code-blocks", "code-friendly", "code-color"])
    formatter = HtmlFormatter(style='xcode')
    css_string = formatter.get_style_defs('.codehilite')

    return render(request, 'blogs/post_detail.html', {'post': post,'posts':posts,'css_string':css_string})


# @login_required(login_url="/logusers/login/")
def blogs_view(request):
    """Main blog view displaying paginated posts and handling comments."""
    items = Items.objects.all()
    courses = Course.objects.all()
    comments = Comment.objects.all()
    post_list = Post.objects.all().order_by('-created_at')  # Order by creation date, most recent first
    paginator = Paginator(post_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    topics = CourseTopic.objects.all()
    form = CommentForm()
    css_string = ""

    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            if request.user.is_authenticated:
                comment.user = request.user
            else:
                comment.user = None  # Or handle it according to model constraints
            comment.save()
            return redirect('blogs:post')

    post_id = request.GET.get('post_id')
    if post_id:
        post = get_object_or_404(Post, id=post_id)
    else:
        post = page_obj.object_list[0] if page_obj.object_list else None

    if post:
        post.body = markdown2.markdown(post.body, extras=["fenced-code-blocks", "code-friendly", "code-color"])
        formatter = HtmlFormatter(style='xcode')
        css_string = formatter.get_style_defs('.codehilite')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and post_id:
        data = {
            'title': post.title,
            'content': post.body,  # Adjust this according to your actual field names
        }
        return JsonResponse(data)

    return render(request, 'blogs/blogpost.html', {
        'courses': courses,
        'topics': topics,
        'page_obj': page_obj,
        'post': post,
        'form': form,
        'post_list':post_list,
        'comments': comments,
        'items': items,
        'css_string': css_string,
        'pygments_css': css_string
    })


def all_courses(request):
    """View displaying all courses."""
    courses = Course.objects.all()
    return render(request, 'blogs/all_courses.html', {'courses': courses})

@login_required(login_url="/logusers/login/")
def my_courses(request):
    """View displaying courses the user is registered for, along with their progress."""
    courses = Course.objects.filter(registered_users=request.user)
    user_course_progress = [
        {
            'course': course,
            'progress': course.overall_progress(request.user)
        }
        for course in courses
    ]
    return render(request, 'blogs/my_courses.html', {'user_course_progress': user_course_progress})


def recent_posts(request):
    """View displaying recent posts with pagination."""
    post_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blogs/recent_posts.html', {'page_obj': page_obj})


@login_required(login_url="/logusers/login/")
def course_topics(request, course_id):
    course = get_object_or_404(Course, id=course_id, registered_users=request.user)
    topic_list = course.coursetopic_set.order_by('date')
    paginator = Paginator(topic_list, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user_progress = UserCourseTopicProgress.objects.filter(user=request.user, topic__course_id=course_id)
    progress_dict = {up.topic_id: up for up in user_progress}
    all_completed = all(progress_dict.get(topic.id, UserCourseTopicProgress()).completed for topic in topic_list)

    # certificate = None
    # if all_completed:
    #     certificate, created = Achievement.objects.get_or_create(title=course.title, user=request.user)
    #     if created:
    #         messages.success(request, f"Congratulations! You've earned the achievement for completing {course.title}.")
    #     else:
    #         messages.info(request, f"You've already earned the achievement for completing {course.title}.")

    return render(request, 'blogs/course_topics.html', {
        'course': course,
       # 'certificate': certificate,
        'page_obj': page_obj,
        'all_completed': all_completed,
        'progress_dict': progress_dict
    })


@login_required(login_url="/logusers/login/")
def mark_topic_complete(request, topic_id):
    """View to mark a course topic as complete."""
    topic = get_object_or_404(CourseTopic, id=topic_id)
    try:
        user_progress, created = UserCourseTopicProgress.objects.get_or_create(user=request.user, topic=topic)
        user_progress.completed = True
        user_progress.progress = 100
        user_progress.save()
        messages.success(request, f"You have successfully completed the topic: {topic.title}")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect('blogs:course_topics', course_id=topic.course.id)



@login_required(login_url="/logusers/login/")
def profile(request):
    """View for updating the user profile."""
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    achievements = Achievement.objects.filter(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('blogs:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProfileForm(instance=profile)

    mycourses = Course.objects.filter(registered_users=user)
    context = {
        'mycourses': mycourses,
        'form': form,
        'user': user,
        'achievements': achievements
    }
    return render(request, 'blogs/profile.html', context)

@login_required(login_url="/logusers/login/")
def download_achievement_view(request, id):
    """View to download an achievement as a PDF."""
    achievement = get_object_or_404(Achievement, id=id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{achievement.title}.pdf"'
    # Generate PDF content here (omitted for brevity)
    return response


@login_required(login_url="/logusers/login/")
def share_achievement_view(request, id):
    """View to share an achievement."""
    achievement = get_object_or_404(Achievement, id=id)
    # Implement share logic here (omitted for brevity)
    return redirect('blogs:profile')



@login_required(login_url="/logusers/login/")
def register_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.user in course.registered_users.all():
        messages.warning(request, 'You are already registered for this course.')
    else:
        course.registered_users.add(request.user)
        messages.success(request, 'You have successfully registered for the course.')
    return redirect('blogs:my_courses')


@login_required(login_url="/logusers/login/")
def unregister_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.user in course.registered_users.all():
        course.registered_users.remove(request.user)
        messages.success(request, 'You have successfully unregistered from the course.')
    else:
        messages.warning(request, 'You are not registered for this course.')
    return redirect('blogs:my_courses')


@login_required(login_url="/logusers/login/")
def course_delete_confirmation_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    context = {'course': course}
    return render(request, 'blogs/confirm_course_deletion.html', context)

@login_required(login_url="/logusers/login/")
def motivation_view(request,course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'blogs/motivation.html',{'course':course})


@login_required(login_url="/logusers/login/")
def take_quiz(request, course_id):
    # Fetch the course object
    course = get_object_or_404(Course, id=course_id)
    topics = CourseTopic.objects.filter(course=course)

    # Filter questions based on the course topics
    questions = Question.objects.filter(topic__in=topics)

    if request.method == 'POST':
        # Collect all the forms
        forms = [UserAnswerForm(request.POST, question=question) for question in questions]

        all_valid = True
        for form in forms:
            if not form.is_valid():
                all_valid = False
                break

        if all_valid:
            for form in forms:
                user_answer, created = UserAnswer.objects.update_or_create(
                    user=request.user,
                    question=form.cleaned_data['question'],
                    defaults={'choice': form.cleaned_data['choice']}
                )
                print(f"Saved answer for question {user_answer.question.id} - Choice: {user_answer.choice.id}")

            return redirect('blogs:quiz_results', course_id=course_id)

    else:
        forms = [UserAnswerForm(question=question) for question in questions]

    return render(request, 'blogs/take_quiz.html', {'forms': forms, 'course': course, 'questions': questions})


@login_required(login_url="/logusers/login/")
def quiz_results(request, course_id):
    questions = Question.objects.filter(course_id=course_id)
    user_answers = UserAnswer.objects.filter(user=request.user, question__course_id=course_id)

    # Debugging: print user answers
    print("User Answers: ", user_answers)

    for answer in user_answers:
        print(f"Question ID: {answer.question.id}, Choice ID: {answer.choice.id}, Is Correct: {answer.choice.is_correct}")

    score = sum(1 for answer in user_answers if answer.choice.is_correct)
    total_questions = questions.count()

    return render(request, 'blogs/quiz_results.html', {
        'score': score,
        'total_questions': total_questions,
        'course_id': course_id,
    })


@login_required(login_url="/logusers/login/")
def add_course_topic(request):
    if request.method == 'POST':
        form = CourseTopicForm(request.POST, request.FILES)
        if form.is_valid():
            course_topic = form.save(commit=False)
            course_topic.user = request.user  # Assign the logged-in user
            course_topic.save()
            return redirect('blogs:post')  # Replace with your view name
    else:
        form = CourseTopicForm()

    return render(request, 'blogs/add_course_topic.html', {'form': form})


@login_required(login_url="/logusers/login/")
def create_blogpost(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.user = request.user
            blog_post.save()
            return redirect('blogs:post')  # Redirect after successful form submission
    else:
        form = PostForm()
    return render(request, 'blogs/create_blogpost.html', {'form': form})

@login_required(login_url="/logusers/login/")

def items_view(request):
    items = Items.objects.all()
    return render(request,'blogs/items.html',{'items':items})


def pofolio(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    return render(request,'blogs/mypofolio.html',{'post':post})


def abdulahcustomerdocument_view(request):
    if request.method == 'POST':
        form = AbdulahCustomerDocumentForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AbdulahCustomerDocumentForm()


    return render(request,'blogs/abdulahdocument.html',{'form':form})





@login_required(login_url="/logusers/login/")
def discusion_forum_home(request,course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    forums = DiscusionForum.objects.filter(course=course)
    topics = ForumTopic.objects.filter(forum__in=forums)
    return render(request, 'blogs/discusion_forum/discustion_forum_home.html', {'topics': topics})



@login_required(login_url="/logusers/login/")
def discusion_topic_detail(request,pk):
    topic = get_object_or_404(ForumTopic, pk=pk)
    if not topic:
        raise Http404("No topics found in this forum")
    posts = topic.posts.all()
    user_has_posted = posts.filter(created_by=request.user).exists()
    return render(request, 'blogs/discusion_forum/new_topic_detail.html', {'topic': topic, 'posts': posts, 'user_has_posted': user_has_posted})



@login_required(login_url="/logusers/login/")
def discusionForumPost_view(request, post_pk):
    post = get_object_or_404(ForumPost, pk=post_pk)
    topic = post.topic
    comments = post.comments.all()
    comment_form = NewCommentForm()

    if request.method == 'POST':
        if 'rating' in request.POST:
            new_discusion_rating(request, post_pk)

        if 'message' in request.POST:
            comment_form = NewCommentForm(request.POST)
            if comment_form.is_valid():
                post = get_object_or_404(ForumPost, pk=post_pk)
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.created_by = request.user
                comment.save()
                return redirect('blogs:discusion_forum_post_view', post_pk=post.pk)


    context = {
        'post': post,
        'topic': topic,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'blogs/discusion_forum/discusionforum_post_view.html', context)


@login_required(login_url="/logusers/login/")
def new_discusion_topic(request):
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.created_by = request.user
            topic.save()
            return redirect('blogs:topic_detail', pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'blogs/discusion_forum/new_discusion_topic.html', {'form': form})

@login_required(login_url="/logusers/login/")
def new_discusion_post(request, pk):
    topic = get_object_or_404(ForumTopic, pk=pk)
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('blogs:discusion_topic_detail', pk=topic.pk)
    else:
        form = NewPostForm()
    return render(request, 'blogs/discusion_forum/new_discusion_post.html', {'form': form, 'topic': topic})


@login_required(login_url="/logusers/login/")
def new_discusion_comment(request, post_pk):
    post = get_object_or_404(ForumPost, pk=post_pk)
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.created_by = request.user
            comment.save()

            return redirect('blogs:discusion_forum_post_view',post_pk=post.pk)

    else:
        form = NewCommentForm()
    return render(request, 'blogs/discusion_forum/new_discusion_comment.html', {'form': form, 'post': post})



@login_required(login_url="/logusers/login/")
def new_discusion_rating(request, post_pk):
    post = get_object_or_404(ForumPost, pk=post_pk)
    if request.method == 'POST':
        form = NewRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.post = post
            rating.created_by = request.user
            rating.save()

            # Calculate new average rating
            post_ratings = post.ratings.all()
            post.average_rating = sum(r.rating for r in post_ratings) / post_ratings.count()
            post.save()

            return redirect('blogs:discusion_forum_post_view', post_pk=post.pk)  # Redirect with post_pk
    else:
        form = NewRatingForm()
    return render(request, 'blogs/discusion_forum/new_discusion_rating.html', {'form': form, 'post': post})

@login_required(login_url="/logusers/login/")
def apply_for_course(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Your application has been submitted successfully.')
            return redirect('blogs:sucess')
        else:
            messages.error(request, 'There was an error with your application. Please check the form and try again.')
    else:
        form = ApplicationForm()

    return render(request, 'blogs/apply_for_course.html', {'form': form})

def sucess_view(request):
    return render(request,'blogs/sucess.html')



def course_questions_view(request, course_id, topic_id):
    course = get_object_or_404(Course, id=course_id)
    topic = get_object_or_404(CourseTopic, id=topic_id, course=course)
    questions = Question.objects.filter(course=course, topic=topic)

    context = {
        'course': course,
        'topic': topic,
        'questions': questions
    }

    return render(request, 'your_template.html', context)



def multi_model_search_view(request):
    query = request.GET.get('query', '')  # Default to empty string if no query

    # Get all objects initially
    posts = Post.objects.all()
    course_topics = CourseTopic.objects.all()
    courses = Course.objects.all()

    if query:
        query_variants = [
            query.strip(),
            query.replace(" ", ""),
            query.lower(),
            query.upper(),
            query.title(),
        ]

        # Filter Posts
        post_filter = Q()
        for variant in query_variants:
            post_filter |= Q(title__icontains=variant) | Q(description__icontains=variant) | Q(body__icontains=variant)
        posts = posts.filter(post_filter)

        # Filter CourseTopics
        course_topic_filter = Q()
        for variant in query_variants:
            course_topic_filter |= Q(title__icontains=variant) | Q(body__icontains=variant)
        course_topics = course_topics.filter(course_topic_filter)

        # Filter Courses
        course_filter = Q()
        for variant in query_variants:
            course_filter |= Q(title__icontains=variant) | Q(type__icontains=variant) | Q(access__icontains=variant)
        courses = courses.filter(course_filter)

    context = {
        'posts': posts,
        'course_topics': course_topics,
        'courses': courses,
        'query': query
    }
    return render(request, 'blogs/multi_model_search.html', context)
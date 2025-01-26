# Example-Data-Skills-Academy---Web-Development-and-Platform-Management
A web application built using Django, designed to manage courses, blogs, discussion forums, and user profiles for an educational platform. It allows users to register for courses, track achievements, and participate in quizzes and discussions.


Data Skills Academy - Web Development and Platform Management
This project is a web application designed for educational purposes, providing features for managing courses, blogs, discussion forums, user profiles, and quizzes. Built with Django, the platform allows users to register for courses, track achievements, and interact with other users in a community-driven environment. It also supports social logins through Google, providing an integrated experience.

Features
User Authentication & Profile Management: Integrated Google OAuth2 login for secure authentication and profile management.
Course Management: Users can register for, view, and track progress in various courses. Course topics can be added and marked as complete.
Discussion Forum: A fully-featured forum for discussions on various topics within courses, where users can create, post, and comment.
Blog Posts: Users can write, create, and manage blog posts related to their learning experiences.
Quiz Management: Users can take quizzes within courses and view quiz results.
User Achievements: Users can download and share their achievements.
Sitemaps & SEO: Supports SEO-friendly URLs and automatic sitemap generation for search engine indexing.
Media Management: Serves media files like images, videos, and PDFs.
Project Structure
arduino
Copy
Edit
├── blogs/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   │   └── blogs/
│   │       ├── home.html
│   │       └── post_detail.html
│   └── urls.py
├── settings.py
├── urls.py
└── requirements.txt
Installation
Follow these steps to run the project locally:

Clone the repository:

bash
Copy
Edit
git clone https://github.com/Abdulahkenneh/Example-Data-Skills-Academy---Web-Development-and-Platform-Management.git
Create a virtual environment:

bash
Copy
Edit
python -m venv env
Activate the virtual environment:

For Windows:
bash
Copy
Edit
.\env\Scripts\activate
For MacOS/Linux:
bash
Copy
Edit
source env/bin/activate
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Set up environment variables:

Create a .env file in the project root and include your Django settings:
text
Copy
Edit
SECRET_KEY='your-secret-key'
DEBUG=True
DATABASE_URL='your-database-url'
Apply migrations:

bash
Copy
Edit
python manage.py migrate
Create a superuser to access the admin panel:

bash
Copy
Edit
python manage.py createsuperuser
Run the development server:



python manage.py runserver
Usage
Navigate to http://127.0.0.1:8000/ to access the platform.
Use the admin panel at http://127.0.0.1:8000/admin/ for managing the platform.
Users can register, login, explore courses, and participate in discussions and quizzes.
URL Structure
Home Page: /
Courses: /all_courses/
Blog Posts: /post/
User Profile: /profile/
Discussion Forum: /discusion-forum-home/<course_pk>/
Quiz: /course/<course_id>/quiz/
Sitemap: /sitemap.xml
Dependencies
Django >= 3.2
django-allauth
django-sitemaps
psycopg2 (for PostgreSQL)
python-decouple (for environment variables)
requests
You can install all dependencies using the following:

bash
Copy
Edit
pip install -r requirements.txt
License
This project is licensed under the MIT License - see the LICENSE file for details.

Author
Abdulahkenneh

Acknowledgments
Django Framework
django-allauth for social login integration
PostgreSQL for database management
Bootstrap for responsive UI design

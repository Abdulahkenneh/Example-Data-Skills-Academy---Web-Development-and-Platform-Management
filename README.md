# Clone-Data-Skills-Academy---Web-Development-and-Platform-Management
A web application built using Django, designed to manage courses, blogs, discussion forums, and user profiles for an educational platform. It allows users to register for courses, track achievements, and participate in quizzes and discussions.



## Features

- **User Authentication & Profile Management**: Integrated Google OAuth2 login for secure authentication and profile management.
- **Course Management**: Users can register for, view, and track progress in various courses. Course topics can be added and marked as complete.
- **Discussion Forum**: A fully-featured forum for discussions on various topics within courses, where users can create, post, and comment.
- **Blog Posts**: Users can write, create, and manage blog posts related to their learning experiences.
- **Quiz Management**: Users can take quizzes within courses and view quiz results.
- **User Achievements**: Users can download and share their achievements.
- **Sitemaps & SEO**: Supports SEO-friendly URLs and automatic sitemap generation for search engine indexing.
- **Media Management**: Serves media files like images, videos, and PDFs.

---

## Project Structure








---

## Installation

Follow these steps to run the project locally:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Abdulahkenneh/Example-Data-Skills-Academy---Web-Development-and-Platform-Management.git
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv env
    ```

3. **Activate the virtual environment**:
    - For Windows:
      ```bash
      .\env\Scripts\activate
      ```
    - For MacOS/Linux:
      ```bash
      source env/bin/activate
      ```

4. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Set up environment variables**:
    - Create a `.env` file in the project root and include your Django settings:
        ```text
        SECRET_KEY='your-secret-key'
        DEBUG=True
        DATABASE_URL='your-database-url'
        ```

6. **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

7. **Create a superuser** to access the admin panel:
    ```bash
    python manage.py createsuperuser
    ```

8. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

---

## Usage

- Navigate to `http://127.0.0.1:8000/` to access the platform.
- Use the admin panel at `http://127.0.0.1:8000/admin/` for managing the platform.
- Users can register, login, explore courses, and participate in discussions and quizzes.

---

## URL Structure

- **Home Page**: `/`
- **Courses**: `/all_courses/`
- **Blog Posts**: `/post/`
- **User Profile**: `/profile/`
- **Discussion Forum**: `/discusion-forum-home/<course_pk>/`
- **Quiz**: `/course/<course_id>/quiz/`
- **Sitemap**: `/sitemap.xml`

---

## Dependencies

- `Django >= 3.2`
- `django-allauth`
- `django-sitemaps`
- `psycopg2` (for PostgreSQL)
- `python-decouple` (for environment variables)
- `requests`

You can install all dependencies using the following:
```bash
pip install -r requirements.txt

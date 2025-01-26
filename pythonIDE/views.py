from django.shortcuts import render, redirect,get_list_or_404
import docker
from .forms import IDE_form,CodeSnippetForm,CodeSnippet,UseraccessForm
import logging
import io
import sys
from django.urls import reverse
from .models import Useraccess
from django.contrib.auth.decorators import login_required
from blogs.models import Profile,Course
from blogs.forms import AccessCodeForm
from django.contrib import messages

# Configure logging to output debug messages
# logging.basicConfig(level=logging.DEBUG)

# def ide_content_execute_view(request):
#     result = None
#     error = None

#     if request.method == 'POST':
#         form = IDE_form(request.POST)
#         if form.is_valid():
#             code = form.cleaned_data['code']
#             client = docker.from_env()
#             try:
#                 logging.debug("Before running the code in the container")
#                 # Run the code in the container
#                 container = client.containers.run(
#                     "python-sandbox",
#                     f"python -c \"{code}\"",
#                     detach=True,
#                     stdin_open=True,
#                     stdout=True,
#                     stderr=True,
#                     auto_remove=True
#                 )
#                 logging.debug("After running the code in the container")
#                 # Wait for the container to finish executing
#                 exit_status = container.wait()
#                 # Capture the logs
#                 result = container.logs(stdout=True, stderr=False).decode('utf-8')
#                 error = container.logs(stdout=False, stderr=True).decode('utf-8')

#             except docker.errors.ContainerError as e:
#                 error = str(e)
#             except docker.errors.ImageNotFound as e:
#                 error = "Docker image not found. Please ensure the image is built and available."
#             except docker.errors.APIError as e:
#                 error = "Docker API error occurred."
#             except Exception as e:
#                 error = str(e)
#                 logging.error(f"An error occurred: {error}")
                
#             # After processing the form, redirect to a success page
#             return redirect('python-ide:execute-ide')  # Replace 'success_page' with the name of your success page URL pattern
#     else:
#         form = IDE_form()

#     logging.debug("Before rendering the template")
#     return render(request, 'pythonIDE/ide.html', {'form': form, 'result': result, 'error': error})


# Configure logging to output debug messages
logging.basicConfig(level=logging.DEBUG)

# client = docker.from_env()


# def execute_code(code):
#     try:
#         logging.debug("Before executing the code")

#         # Create a Docker container for isolated execution
#         container = client.containers.run(
#             image="python:3.9",  # Choose an appropriate Python Docker image
#             command="python3 -c 'exec(\"\"\"{}\"\"\")'".format(code),
#             detach=True,
#             mem_limit='100m',  # Limit memory usage
#             cpu_period=100000,
#             cpu_quota=50000,  # Limit CPU usage
#             network_disabled=True,  # Disable network access for security
#             stderr=True,
#             stdout=True,
#         )
#         exit_code = container.wait(timeout=10)
#         output = container.logs().decode("utf-8")

#         # Clean up the container
#         container.remove()

#         if exit_code != 0:
#             logging.error(f"Execution error: {output}")
#             return None, output

#         logging.debug(f"Execution result: {output}")
#         return output, None
#     except Exception as e:
#         error = str(e)
#         logging.error(f"An error occurred: {error}")
#         return None, error


# @login_required(login_url="/login/")
# def ide_view(request):
#     result = None  # Define result variable with a default value
#     error = None  # Define error variable with a default value

#     if request.method == 'POST':
#         form = CodeSnippetForm(request.POST)
#         if form.is_valid():
#             code = form.cleaned_data['code']
#             result, error = execute_code(code)
#             if error is None:
#                 # Save code snippet to database
#                 form.save()
#         else:
#             logging.debug("Form is not valid")
#     else:
#         form = CodeSnippetForm()

#     logging.debug(f"Before rendering the template - Result: {result}, Error: {error}")
#     return render(request, 'pythonIDE/ide.html', {'form': form, 'result': result, 'error': error})

# def restricted_exec(code):
#     allowed_builtins = {
#         'print': print,
#         'str': str,
#         'int': int,
#         'float': float,
#         'bool': bool,
#         'len': len,
#         'range': range,
#         'abs': abs,
#         'sum': sum,
#         'min': min,
#         'max': max,
#         # Add other allowed built-ins as needed
#     }

#     exec_globals = {
#         '__builtins__': allowed_builtins,
#     }

#     exec_locals = {}

#     # Redirect stdout to capture print statements
#     old_stdout = sys.stdout
#     redirected_output = sys.stdout = io.StringIO()

#     try:
#         exec(code, exec_globals, exec_locals)
#         result = redirected_output.getvalue()
#         sys.stdout = old_stdout

#         if not result.strip():
#             result = 'Code executed successfully but no result to display.'

#         return result, None
#     except Exception as e:
#         sys.stdout = old_stdout
#         error = ''.join(traceback.format_exception(None, e, e.__traceback__))
#         return None, error

# def ide_view(request):
#     result = None  # Define result variable with a default value
#     error = None   # Define error variable with a default value

#     if request.method == 'POST':
#         form = CodeSnippetForm(request.POST)
#         if form.is_valid():
#             code = form.cleaned_data['code']
#             result, error = restricted_exec(code)
#             if error is None:
#                 # Save code snippet to database
#                 form.save()
#         else:
#             logging.debug("Form is not valid")
#     else:
#         form = CodeSnippetForm()
    
#     logging.debug(f"Before rendering the template - Result: {result}, Error: {error}")
#     return render(request, 'pythonIDE/ide.html', {'form': form, 'result': result, 'error': error})

# # Add security headers to the response
# def add_security_headers(response):
#     response['Content-Security-Policy'] = "default-src 'self'; script-src 'self' https://cdn.jsdelivr.net;"
#     response['X-Content-Type-Options'] = 'nosniff'
#     response['X-Frame-Options'] = 'DENY'
#     response['X-XSS-Protection'] = '1; mode=block'
#     return response



import threading
from RestrictedPython import compile_restricted, safe_globals, utility_builtins, limited_builtins
from RestrictedPython.Eval import default_guarded_getitem, default_guarded_getiter

def _print(*args):
    print(*args)
    
def execute_code(code, timeout=5):
    def target():
        nonlocal result, error
        try:
            logging.debug("Before executing the code")

            # Redirect stdout to capture print statements
            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()

            # Compile the code using RestrictedPython
            compiled_code = compile_restricted(code, '<string>', 'exec')

            # Define the execution environment
            exec_globals = {
              #  '_getitem_': default_guarded_getitem,
             #   '_getiter_': default_guarded_getiter,

            }

            exec(compiled_code, exec_globals, {})

            # Reset stdout
            sys.stdout = old_stdout

            # Capture printed output
            printed_output = redirected_output.getvalue()

            logging.debug(f"Execution result: {printed_output}")
            result = printed_output
        except Exception as e:
            error = str(e)
            logging.error(f"An error occurred: {error}")

    result = None
    error = None
    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        error = "Code execution timed out."
        logging.error(error)
        thread.join()  # Ensure thread has stopped

    return result, error

@login_required(login_url="/logusers/login/")
def ide_view(request):
    result = None  # Define result variable with a default value
    error = None   # Define error variable with a default value

    if request.method == 'POST':
        form = CodeSnippetForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            result, error = execute_code(code)
            if error is None:
                # Save code snippet to database
                form.save()
            else:
                logging.debug(f"Code execution error: {error}")
        else:
            logging.debug("Form is not valid")
    else:
        form = CodeSnippetForm()
    
    logging.debug(f"Before rendering the template - Result: {result}, Error: {error}")
    return render(request, 'pythonIDE/ide.html', {'form': form, 'result': result, 'error': error})

from django.http import HttpResponse
def home(request):
    return HttpResponse('Welcome to Amazon')



 


#Granting access to special useer
@login_required(login_url="/logusers/login/")
def access_code_view(request):
    if request.method == 'POST':
        form = AccessCodeForm(request.POST)
        if form.is_valid():
            access_code = form.cleaned_data.get('access_code')
            try:
                user_profile = Profile.objects.get(user=request.user)
                if user_profile.access_code == access_code:
                    request.session['access_granted'] = True
                    return redirect('python-ide:ide')
                else:
                    messages.error(request, 'Invalid access code.')
            except Profile.DoesNotExist:
                messages.error(request, 'User profile not found.')
    else:
        form = AccessCodeForm()
    return render(request, 'pythonIDE/access_code.html', {'form': form})



@login_required(login_url='/login/')
def user_access_code_view(request, course_id):
    course = get_list_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = UseraccessForm(request.POST)
        if form.is_valid(): 
            access_code = form.cleaned_data.get('access_code')  # Correctly access cleaned_data
            try:
                user_access = Useraccess.objects.get(user=request.user)
                if user_access.access_code == access_code:  # Correctly compare access codes
                    request.session['user_access_granted'] = True  # Use consistent session variable name
                    print('User access granted')  # Debugging
                    return redirect(reverse('blogs:register_course', args=[course_id]))
                else:
                    messages.error(request, 'Invalid access code')
                    print('Invalid access code')  # Debugging
            except Useraccess.DoesNotExist:
                messages.error(request, "You don't have access ")
                print("User access does not exist")  # Debugging
        else:
            print('Form is not valid')  # Debugging
    else:
        form = UseraccessForm()
  
    return render(request, 'pythonIDE/useraccess.html', {'form': form, 'course': course})
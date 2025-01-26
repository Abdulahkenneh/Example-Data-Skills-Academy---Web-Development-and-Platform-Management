from django.http import HttpResponsePermanentRedirect
from datetime import datetime
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin

class RedirectToWWW:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if not host.startswith('www.'):
            new_url = request.build_absolute_uri().replace(host, 'www.' + host)
            return HttpResponsePermanentRedirect(new_url)
        return self.get_response(request)




class ActiveUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            User = get_user_model()
            user = User.objects.get(pk=request.user.pk)
            user.last_login = datetime.now()
            user.save()
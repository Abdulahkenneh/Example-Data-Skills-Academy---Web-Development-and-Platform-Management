from django.shortcuts import redirect

def access_code_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('access_granted', False):
            return redirect('pythonIDE:access_code')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def user_access_code_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('user_access_granted', False):
            return redirect('python-ide:user_access_code')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
from functools import wraps
from django.shortcuts import redirect

def group_required(*group_names):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
            else:
                return redirect('perm_error')
        return _wrapped_view
    return decorator
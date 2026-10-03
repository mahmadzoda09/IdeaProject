from django.shortcuts import redirect

def login_required(func):
    def required(request,*args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return func(request,*args, **kwargs)
    return required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

from django.shortcuts import redirect

class SigninView(LoginView):
    template_name = 'home/login.html'

    def get(self, request, *args, **kwargs):     # overriding this method redirects to indicated website when authenticated
        if self.request.user.is_authenticated:
            return redirect('portal/')
        return super().get(request, *args, **kwargs)

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'home/signup.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('portal/')
        return super().get(request, *args, **kwargs)

class LogoutInterfaceView(LogoutView):
    template_name = 'home/logout.html'

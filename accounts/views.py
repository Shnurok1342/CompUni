from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from .forms import LoginForm

# Create your views here.
class LoginView(TemplateView):
    login_form = None
    template_name = "accounts/login.html"

    def get(self, request, *args, **kwargs):
        self.login_form = LoginForm()
        return super(LoginView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context["login_form"] = self.login_form
        return context

    def post(self, request, *args, **kwargs):
        self.login_form = LoginForm(request.POST)
        if self.login_form.is_valid():
            user = authenticate(username = self.login_form.cleaned_data["username"],
                                password = self.login_form.cleaned_data["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/products/")
                else:
                    return super(LoginView, self).get(request, *args, **kwargs)
            else:
                return super(LoginView, self).get(request, *args, **kwargs)
        else:
            return super(LoginView, self).get(request, *args, **kwargs)

class LogoutView(TemplateView):
    template_name = "accounts/logout.html"

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("/products/")
        # return super(LogoutView, self).get(request, *args, **kwargs)

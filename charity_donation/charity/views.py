from django.shortcuts import render

# Create your views here.
from django.views import View


class HomeView(View):
    def get(self, request):
        return render(request, "index.html")


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")


class FormView(View):
    def get(self, request):
        return render(request, "form.html")


class ConfirmationView(View):
    def get(self, request):
        return render(request, "form-confirmation.html")

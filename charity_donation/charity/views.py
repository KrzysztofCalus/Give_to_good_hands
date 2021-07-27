from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.
from django.views import View

from charity.models import Donation, Institution


def logout_view(request):
    logout(request)
    return redirect('landing')


class HomeView(View):
    def get(self, request):
        quantity = Donation.objects.aggregate(Sum('quantity'))
        institution = Institution.objects.count()
        fundacja = Institution.objects.filter(type='fundacja')
        organizacja = Institution.objects.filter(type='organizacja pozarządowa')
        zbiorka = Institution.objects.filter(type='zbiórka lokalna')
        return render(request, "index.html", {'quantity': quantity,
                                              'institution': institution,
                                              'fundacja': fundacja,
                                              'organizacja': organizacja,
                                              'zbiorka': zbiorka})


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if password == password2:
            User.objects.create_user(username=email, email=email, password=password,
                                     first_name=name, last_name=surname)
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username_to_check = request.POST.get("email")
        password_to_check = request.POST.get("password")
        user = authenticate(username=username_to_check, password=password_to_check)
        if user is not None:
            login(request, user)
            return redirect('landing')
        else:
            return redirect('register')


# class LogoutView(View):
#     def logout_view(self, request):
#         logout(request)
        # return redirect('login')

    # def get(self, request):
    #     logout(request)
    #     return redirect('login')


class FormView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "form.html")


class ConfirmationView(View):
    def get(self, request):
        return render(request, "form-confirmation.html")

from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


# Create your views here.
from django.views import View

from charity.models import Donation, Institution


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


class FormView(View):
    def get(self, request):
        return render(request, "form.html")


class ConfirmationView(View):
    def get(self, request):
        return render(request, "form-confirmation.html")

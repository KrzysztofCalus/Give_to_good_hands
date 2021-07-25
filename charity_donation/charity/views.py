from django.db.models import Sum
from django.shortcuts import render


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


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")


class FormView(View):
    def get(self, request):
        return render(request, "form.html")


class ConfirmationView(View):
    def get(self, request):
        return render(request, "form-confirmation.html")

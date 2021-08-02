from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import View

from .models import Donation, Institution, Category


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


class FormView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, "form.html", {'categories': categories,
                                             'institutions': institutions})

    def post(self, request):
        categories = request.POST.getlist("categories")
        bags = request.POST.get("bags")
        organization = request.POST.get("organization")
        address = request.POST.get("address")
        city = request.POST.get("city")
        postcode = request.POST.get("postcode")
        phone = request.POST.get("phone")
        data = request.POST.get("data")
        time = request.POST.get("time")
        more_info = request.POST.get("more_info")
        user = self.request.user.id
        for category in categories:
            Donation.objects.create(quantity=bags, institution=organization, address=address,
                                    phone_number=phone, city=city, zip_code=postcode,
                                    pick_up_date=data, pick_up_time=time,
                                    pick_up_comment=more_info,
                                    user_id=user, categories=category)
        return redirect('confirmation')


class ConfirmationView(View):
    def get(self, request):
        return render(request, "form-confirmation.html")


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        users = self.request.user
        donations = Donation.objects.filter(user_id=self.request.user.id)
        return render(request, "profile.html", {"users": users,
                                                "donations": donations})

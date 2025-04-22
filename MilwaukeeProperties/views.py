from django.shortcuts import render
from .models import *
from django.views import View



# Create your views here.
class HomeView(View):
    def get(self, request):
        sales = Sale.objects.all()
        return render(request, 'home.html', {
            'sales': sales,
        })

class LoginView(View):
    def get(self, request):

class PropertyView(View):
    def get(self, request):

class SearchView(View):
    def get(self, request):

class FavoritesView(View):
    def get(self, request):

class RealtorView(View):
    def get(self, request):

class DistrictView(View):
    def get(self, request):


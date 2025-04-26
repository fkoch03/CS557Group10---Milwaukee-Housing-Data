from django.shortcuts import render
from .models import *
from django.views import View



# Create your views here.
class HomeView(View):
    def get(self, request, user_id):
        sales = Sale.objects.all()
        user = User.objects.get(id=user_id)
        return render(request, 'home.html', {
            'sales': sales,
            'user':user
        })

class LoginView(View):
    def login_view(request):
        if request.method == "POST":
            username = request.POST.get('username')
            email = request.POST.get('email')

            try:
                user = User.objects.get(username=username, email=email)
                return redirect('home')
            except User.DoesNotExist:
                error_message = "Invalid username or email. Please try again."
                return render(request, 'login.html', {'error_message': error_message})
        return render(request, "login.html")

class PropertyView(View):
    def get(self, request, property_id):
        sales = Sale.objects.filter(property_id=property_id)
        prop = Property.objects.get(id=property_id)
        comments = Comment.objects.filter(property_id=property_id)
        details = {
            "Neighborhood": prop.nbhd.nbhd,
            "Style": prop.style,
            "Exterior Wall": prop.extwall,
            "Stories": prop.stories,
            "Year Built": prop.year_built,
            "Rooms": prop.rooms,
            "Finished Sq Ft": prop.finished_sqft,
            "Units": prop.units,
            "Full Baths": prop.full_bath,
            "Half Baths": prop.half_bath,
            "Lot Size": prop.lot_size,
        }

        affiliates = [
            {"title": "Realtor", "name": f"{prop.realtor.first_name} {prop.realtor.last_name}"},
            {"title": "Company", "name": prop.realtor.company.name if prop.realtor.company else "N/A"},
        ]
        return render(request, 'property.html', {
            'sales': sales,
            'prop': prop,
            'comments': comments,
            'details': details,
            'affiliates': affiliates,
        })

class SearchView(View):
    def get(self, request):

class FavoritesView(View):
    def get(self, request):

class RealtorView(View):
    def get(self, request):

class DistrictView(View):
    def get(self, request):


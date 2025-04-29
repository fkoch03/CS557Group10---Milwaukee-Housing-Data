from django.shortcuts import render
from .models import *
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


# Create your views here.
class HomeView(View):
    def get(self, request):
        sales = Sale.objects.all()
        return render(request, 'home.html', {
            'sales': sales,
        })

# class LoginView(View):
#     def get(self, request):
#         return render(request, 'login.html', )
#
#     def login_view(request):
#         if request.method == "POST":
#             username = request.POST.get('username')
#             email = request.POST.get('email')
#
#             try:
#                 user = User.objects.get(username=username, email=email)
#                 return redirect('home')
#             except User.DoesNotExist:
#                 error_message = "Invalid username or email. Please try again."
#                 return render(request, 'login.html', {'error_message': error_message})
#         return render(request, "login.html")

class PropertyView(View):
    def get(self, request, property_id):
        try:
            prop = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return render(request, 'noresult.html')
        sales = Sale.objects.filter(property_id=property_id)
        comments = Comment.objects.filter(property_id=property_id)
        location = Location.objects.get(id=prop.prop_id_id)
        details = {
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
        return render(request, 'property.html', {
            'sales': sales,
            'prop': prop,
            'comments': comments,
            'details': details,
            'location' : location,
        })

class SearchView(View):
    def get(self, request):
        return

class FavoritesView(View):
    def get(self, request):
        return


class RealtorView(View):
    def get(self, request):
        return


class DistrictView(View):
    def get(self, request):
        return

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
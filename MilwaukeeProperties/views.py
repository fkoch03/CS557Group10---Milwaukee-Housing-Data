import datetime

from django.shortcuts import render, redirect
from .models import *
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
import random
from .forms import *

# Create your views here.
class HomeView(View):
    def get(self, request):
        random_sale = random.randint(0,400)
        sales = Sale.objects.all()[random_sale:random_sale+12]
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
class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm


class PropertyView(View):
    def get(self, request, property_id):
        try:
            prop = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return render(request, 'noresult.html')
        sales = Sale.objects.filter(property_id=property_id)
        comments = Comment.objects.filter(property_id=property_id)
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
        })
    def post(self, request, property_id):
        if request.user.is_authenticated:

            if 'add_to_favourites' in request.POST:
                Favorite.objects.create(user=request.user, property_id=property_id, date=datetime.datetime.now())
            elif 'add_comment' in request.POST:
                comment_content = request.POST.get('comment')
                if comment_content:
                    Comment.objects.create(
                        user=request.user,
                        property_id=property_id,
                        comment=comment_content,
                        date=datetime.datetime.now()
                    )
            return redirect('property', property_id=property_id)
        return redirect('login')
            # Favorite.objects.create(user=request.user.id, property=property_id, date=datetime.datetime.now())
            # redirect('property', property_id=property_id)



class SearchView(View):
    def get(self, request):
        styles = Property.objects.values_list('style', flat=True).distinct().order_by('style')
        sales = Sale.objects.select_related('property').all()[:48]
        return render(request, 'search.html', {
            'sales': sales,
            'styles': styles,
        })

    def post(self, request):
        search_bar = request.POST.get("search_bar")
        property_type = request.POST.get("property_type")
        min_price = request.POST.get("min_price")
        max_price = request.POST.get("max_price")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        sales = Sale.objects.select_related('property').all()

        if search_bar:
            sales = sales.filter(property__prop_id__address__icontains=search_bar)
        if property_type:
            sales = sales.filter(property__style=property_type)

        try:
            if min_price:
                sales = sales.filter(price__gte=int(min_price))
            if max_price:
                sales = sales.filter(price__lte=int(max_price))
        except ValueError:
            pass

        if start_date:
            sales = sales.filter(date__gte=start_date)
        if end_date:
            sales = sales.filter(date__lte=end_date)

        styles = Property.objects.values_list('style', flat=True).distinct().order_by('style')
        return render(request, 'search.html', {
            'sales': sales[:48],
            'styles': styles,
        })


class FavoritesView(View):
    def get(self, request):
        if request.user.is_authenticated:
            favorites = Favorite.objects.filter(user_id=request.user.id)
            return render(request, 'favorites.html', {
                'favorites': favorites,
            })
        else:
            random_sale = random.randint(0, 400)
            sales = Sale.objects.all()[random_sale:random_sale + 12]
            return render(request, 'home.html', {
                'sales': sales,
                'message': 'Log in or create an account to see your favorites!',
            })



class RealtorView(View):
    def get(self, request):
        return


class DistrictView(View):
    def get(self, request):
        return

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
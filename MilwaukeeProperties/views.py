import datetime
from symbol import continue_stmt

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

        is_favorite = False
        if request.user.is_authenticated:
            property = Property.objects.get(id=property_id)
            is_favorite = Favorite.objects.filter(user=request.user, property=property).exists()

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
            "District": prop.district.name,
            "Taxkey" : prop.taxkey,
            "Latitude" : prop.prop_id.latitude,
            "Longitude" : prop.prop_id.longitude,
        }
        condo = False
        if prop.condo.id != 1:
            condo = True

        return render(request, 'property.html', {
            'user' : request.user,
            'sales': sales,
            'prop': prop,
            'comments': comments,
            'details': details,
            'is_favorite' : is_favorite,
            'condo': condo,
        })
    def post(self, request, property_id):
        if request.user.is_authenticated:
            property = Property.objects.get(id=property_id)

            if 'add_to_favorites' in request.POST:
                if Favorite.objects.filter(property_id=property_id).exists():
                    return redirect('property', property_id=property_id)
                Favorite.objects.create(user=request.user, property=property, date_added=datetime.datetime.now())
            elif 'remove_from_favorites' in request.POST:
                if Favorite.objects.filter(property_id=property_id).exists():
                    Favorite.objects.filter(property_id=property_id).delete()
            elif 'add_comment' in request.POST:
                comment_content = request.POST.get('comment')
                if comment_content:
                    Comment.objects.create(
                        user=request.user,
                        property_id=property_id,
                        comment=comment_content,
                        date=datetime.datetime.now()
                    )
            elif 'delete_comment' in request.POST:
                comment_id = request.POST.get('comment_id')
                if comment_id:
                    Comment.objects.filter(id=comment_id).delete()
            elif 'save_comment' in request.POST:
                comment_id = request.POST.get('comment_id')
                if comment_id:
                    comment = Comment.objects.get(id=comment_id)
                    comment.comment = request.POST.get('updated_comment')
                    comment.save()
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
    def post(self, request):
        if request.user.is_authenticated:
            if 'delete_favorite' in request.POST:
                fav_id = request.POST.get('fav_id')
                if fav_id:
                    Favorite.objects.filter(id=fav_id).delete()
            return redirect('favorites')



class RealtorView(View):
    def get(self, request, realtor_id):
        realtor = Realtor.objects.get(id=realtor_id)
        sales = Sale.objects.filter(realtor_id=realtor_id)
        return render(request, 'realtor.html', {
            'realtor': realtor,
            'sales': sales,
        })


class DistrictView(View):
    def get(self, request, district_id):
        district = District.objects.get(id=district_id)
        sales = Sale.objects.filter(property__district_id=district_id)[:24]
        return render(request, 'district.html', {
            'district': district,
            'sales': sales,
        })

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class CondoView(View):
    def get(self, request, condo_id):
        if CondoProject.objects.filter(id=condo_id) :
            condo = CondoProject.objects.get(id=condo_id)
            sales = Sale.objects.filter(property__condo_id=condo_id)
            return render(request, 'condo.html', {
                "condo" : condo,
                "sales" : sales,
            })
        return render(request, 'noresult.html')

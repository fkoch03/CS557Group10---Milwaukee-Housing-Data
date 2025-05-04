from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Max

from MilwaukeeProperties.models import Property, Sale


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}),
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}),
        label='Password'
    )

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}),
        label="Username"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm Password'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

##This is garbage, don't use VVV
class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        styles = Property.objects.values_list('style', flat=True).distinct().order_by('style')
        style_choices = [(style, style) for style in styles if style]  # exclude null/blank if needed

        self.fields['style_dropdown'] = forms.ChoiceField(
            choices=style_choices,
            widget=forms.Select(attrs={
                'size': 10,
                'style': 'overflow-y: auto; height: 200px;'
            }),
            required=False
        )

        max_price = Sale.objects.aggregate(Max('price'))
        step = 25000
        price_points = list(range(0, int(max_price + step), step))
        price_choices = [(p, f"${p:,.0f}") for p in price_points]

        self.fields['min_price'] = forms.ChoiceField(
            choices=[('', 'No Min')] + price_choices,
            widget=forms.Select(attrs={'style': 'width: 150px;'}),
            required=False
        )
        self.fields['max_price'] = forms.ChoiceField(
            choices=[('', 'No Max')] + price_choices,
            widget=forms.Select(attrs={'style': 'width: 150px;'}),
            required=False
        )
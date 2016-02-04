from django import forms
from .models import Account
from .models import AccountAddon


class Accounts_Form(forms.ModelForm):

    class Meta:
        model = Account
        widgets = {
                  'schedule': forms.Textarea(attrs={'rows': 2}),
                }
        fields = ('id', 'name', 'billingstreet', 'billingcity',
                  'billingstate', 'billingcountry',
                  'geolocation_longitude_s', 'geolocation_latitude_s',
                  'createddate')


class AccountsAddons_Form(forms.ModelForm):

    class Meta:
        model = AccountAddon
        fields = ('schedule', 'is_featured',
                  'avg_consumer_spending',
                  'menu_best_sellers', 'promotions',)

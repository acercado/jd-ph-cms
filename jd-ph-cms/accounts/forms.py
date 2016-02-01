from django import forms
from .models import AccountAddon


class AccountsAddons_Form(forms.ModelForm):

    class Meta:
        model = AccountAddon
        fields = ('schedule', 'is_featured',
                  'avg_consumer_spending',
                  'menu_best_sellers', 'promotions',)

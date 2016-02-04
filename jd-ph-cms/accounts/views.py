from django.http import HttpResponse
from django.db.models import Q, Sum, Count
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Account
from .models import AccountAddon
from ..productofferings.models import ProductOffering

from .forms import Accounts_Form
from .forms import AccountsAddons_Form
from ..productofferings.forms import Product_Offerings_Form

from ..utils import send_notifications


def index(request):
    # return HttpResponse('Testing lung...')
    accounts_obj = Account.objects.filter(Q(accountaddons__isnull=True)|Q(accountaddons__isnull=False)).order_by('name')
    print('Queryset: ', accounts_obj.query)
    return render(request, 'accounts/index.html', {'accounts': accounts_obj})


def something(request):
    return HttpResponse('this is something, hmmm...')


@login_required
def edit(request, pk):
    # should be already existing
    mode = ""
    account_obj = get_object_or_404(Account, pk=pk)

    box_status = 'closed'
    '''
        Instantiate account addon object first, create one if not yet existing
    '''

    try:
        account_addon_obj = AccountAddon.objects.get(account=account_obj)
        form_account_addon = AccountsAddons_Form(request.POST, instance=account_addon_obj)
    except AccountAddon.DoesNotExist:
        form_account_addon = AccountsAddons_Form(request.POST)
        account_addon_obj = form_account_addon.save(commit=False)
        account_addon_obj.account = account_obj
        account_addon_obj.author = request.user
        account_addon_obj.last_update_datetime = timezone.now()
        account_addon_obj.save()

    if request.method == 'POST':

        if 'btn_save_account_info' in request.POST:

            notif = request.POST.get('make_notif')
            '''
                revalidate new account addon user supplied values
            '''
            # form_account_addon = AccountsAddons_Form(request.POST, instance=account_addon_obj)

            if form_account_addon.is_valid():
                account_addon_obj = form_account_addon.save(commit=False)
                account_addon_obj.account = account_obj
                account_addon_obj.author = request.user
                account_addon_obj.last_update_datetime = timezone.now()
                account_addon_obj.save()
                form_account_addon = AccountsAddons_Form(instance=account_addon_obj)
                mode = 'saved'

                '''
                    create notify object if needed
                '''

                
                print('Notif: %s' % notif)

                if account_addon_obj.has_notif:
                    if notif == None:
                        print('Delete notif here')
                        send_notifications('account', account_obj, None, None, True)
                    else:
                        send_notifications('account', account_obj)
                else:
                    if notif != None:
                        send_notifications('account', account_obj)

            form_prod_offers = Product_Offerings_Form()

        elif 'btn_add_product' in request.POST:
            '''
                create product offer objects here
            '''
            form_prod_offers = Product_Offerings_Form(request.POST, request.FILES)
            
            if form_prod_offers.is_valid():
                prod_offers = form_prod_offers.save(commit=False)
                prod_offers.author = request.user
                prod_offers.account = account_obj
                prod_offers.save()
                mode = 'saved'
            else:
                box_status = 'open'


    else:
        form_account_addon = AccountsAddons_Form(instance=account_addon_obj)
        form_prod_offers = Product_Offerings_Form()
    
    form_account = Accounts_Form(instance=account_obj)
    products = ProductOffering.objects.filter(account=account_obj)

    return render(request , 'accounts/new.html',
        {'form': form_account, 'form_addon': form_account_addon, 'notif': account_addon_obj,
        'form_products_input': form_prod_offers, 'form_products': products,
        'prod_offer_box': box_status,
        'mode': mode})
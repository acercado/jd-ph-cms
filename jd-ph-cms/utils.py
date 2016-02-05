from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta
from .policies.models import Policy
from .notifications.models import NotificationMessage
from .rewards.models import Reward
from .users.models import User


def check_policy_existance():
    try:
        policy_obj = Policy.objects.all()[:1].get()
    except Policy.DoesNotExist:
        # create the record if it does not exists yet
        # with default values
        current_datetime = timezone.now().strftime('%Y-%m-%d %I:%M %p')
        current_datetime = datetime.strptime(current_datetime,'%Y-%m-%d %I:%M %p')
        date_end = current_datetime + timedelta(days=1)

        admin_user = User.objects.get(is_superuser=1)

        policy_obj = Policy(
            news_duration_date_start = current_datetime,
            news_duration_date_end = date_end,
            contests_duration_date_start = current_datetime,
            contests_duration_date_end = date_end,
            max_answers_per_question = settings.POLICY_MAX_ANSWERS_PER_QUESTION,
            messages_new_account = settings.NOTIF_MESSAGE_NEW_ACCOUNT,
            messages_new_loyalty_item = settings.NOTIF_MESSAGE_NEW_LOYALTY_ITEM,
            messages_new_contest = settings.NOTIF_MESSAGE_NEW_CONTEST,
            messages_winner = settings.NOTIF_MESSAGE_WINNER,
            last_update_by_author = admin_user,
            last_update_datetime = timezone.now(),
            admin_email = settings.POLICY_ADMIN_EMAIL,
            country = settings.POLICY_DEFAULT_COUNTRY,
        )
        policy_obj.save()
    return policy_obj


def send_notifications(category, ref_obj=None, web_user_obj=None, prizes=None, delete=False):
    # category: contest, winner, account, loyalty/reward item
    # first check if there's actually a policy message definition
    policy_obj = check_policy_existance() # Policy.objects.all()[:1].get()

    if category=='contest':
        notif_message = policy_obj.messages_new_contest if policy_obj.messages_new_contest else ""
        message_new_contest = notif_message.replace("[contest_name]", ref_obj.name)
        parsed_policy_message = message_new_contest
    elif category=='winner':
        prize_item = prizes.split(',')
        prizes = []
        for item in prize_item:
            prizes.append(item.strip())
        prizes_obj = Reward.objects.filter(id__in=prizes)
        prizes = ""
        for item in prizes_obj:
            prizes += item.name + ", "
        prizes = prizes[:-2]

        notif_message = policy_obj.messages_winner if policy_obj.messages_winner else ""
        salesrep_no = policy_obj.salesrep_no
        notif_message = notif_message.replace("[user_name]", web_user_obj.name)
        notif_message = notif_message.replace("[reward_item]", prizes)
        parsed_policy_message = notif_message.replace("[salesrep_no]", salesrep_no)
        title = "Contest Winner"
        linkback = "contest_winner_" + str(ref_obj.id)
    elif category=='account':
        notif_message = policy_obj.messages_new_account if policy_obj.messages_new_account else ""
        parsed_policy_message = notif_message.replace("[acct_name]", ref_obj.name)
        build_address = ref_obj.billingstreet + ', ' + ref_obj.billingcity + ', ' + ref_obj.billingstate + ', ' + ref_obj.billingcountry
        parsed_policy_message = parsed_policy_message.replace("[acct_addr]", build_address)
        title = "New Store Opens!"
        linkback = 'new_account_' + str(ref_obj.id)
    elif category=='reward':
        notif_message = policy_obj.messages_new_loyalty_item if policy_obj.messages_new_loyalty_item else ""
        notif_message = notif_message.replace("[reward_item]", ref_obj.name)
        notif_message = notif_message.replace("[reward_info]", ref_obj.details)
        parsed_policy_message = notif_message.replace("[reward_value]", str(ref_obj.value))
        title = "New Reward Item!"
        linkback = 'new_reward_' + str(ref_obj.id)

    if parsed_policy_message.strip() == '':
        delete = True

    if delete:
        try:
            notif_obj = NotificationMessage.objects.get(linkback = linkback)
            notif_obj.delete()
        except NotificationMessage.DoesNotExist:
            pass
    else:
        # create notifications
        if category!='winner':
            notif_obj, created = NotificationMessage.objects.update_or_create(
                            linkback = linkback,
                            defaults = {
                                'title' : title,
                                'message' : parsed_policy_message,
                                'category': category
                            }
                    )
        else:
            notif_obj, created = NotificationMessage.objects.update_or_create(
                            linkback = linkback,
                            defaults = {
                                'title' : title,
                                'message' : parsed_policy_message,
                                'category': category,
                                'user': web_user_obj
                            }
                    )

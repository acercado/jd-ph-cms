from .policies.models import Policy
from .notifications.models import NotificationMessage
from .rewards.models import Reward


def send_notifications(category, ref_obj=None, web_user_obj=None, prizes=None, delete=False):
    # category: contest, winner, account, loyalty/reward item 
    # first check if there's actually a policy message definition
    policy_obj = Policy.objects.all()[:1].get()
    
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

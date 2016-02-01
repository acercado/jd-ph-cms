from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from ..users.models import User


class Policy(models.Model):
    news_duration_date_start = models.DateTimeField(blank=True, null=True)
    news_duration_date_end = models.DateTimeField(blank=True, null=True)
    contests_duration_date_start = models.DateTimeField(blank=True, null=True)
    contests_duration_date_end = models.DateTimeField(blank=True, null=True)
    max_answers_per_question = models.PositiveSmallIntegerField(default=1,validators=[MinValueValidator(1)])
    map_radius = models.PositiveSmallIntegerField(default=500,validators=[MinValueValidator(1)])
    admin_email = models.CharField(default=settings.POLICY_ADMIN_EMAIL,
                                   max_length=100)
    messages_new_account = models.TextField(blank=True, null=True)
    messages_new_contest = models.TextField(blank=True, null=True)
    messages_new_loyalty_item = models.TextField(blank=True, null=True)
    messages_winner = models.TextField(blank=True, null=True)
    last_update_by_author = models.ForeignKey(User, null=True, blank=True)
    last_update_datetime = models.DateTimeField(null=True, blank=True)
    claiming_method = models.CharField(
        max_length=200,
        null=True,
        blank=True)
    country = models.CharField(
        choices=settings.POLICY_COUNTRY,
        default='Philippines',
        max_length=15,
        blank=True)
    salesrep_no = models.CharField(max_length=200, null=True, blank=True)
    policy_name = 'policy_news'

    class Meta:
        verbose_name_plural = 'Policies'
        db_table = 'cms_policy'

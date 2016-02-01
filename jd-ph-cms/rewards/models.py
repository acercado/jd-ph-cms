from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from cloudinary.models import CloudinaryField
from ..users.models import User


class Reward(models.Model):
    name = models.CharField(max_length=200)
    details = models.TextField()
    reward_type = models.CharField(
        choices=settings.PERKS_AND_PRIZES_REWARD_TYPE_CHOICES,
        default='Perks & Prize',
        max_length=20)
    value = models.PositiveSmallIntegerField(default=0,validators=[MinValueValidator(0)])
    icon = CloudinaryField('icon')
    is_active = models.BooleanField(default=True)
    is_type = models.CharField(default='Rewards', max_length=50)
    is_featured = models.BooleanField(default=False)
    author = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, null=True, blank=True, default='rewards')
    # possible phase 2
    # inventory_count = models.PositiveSmallIntegerField(default=1,validators=[MinValueValidator(1)])

    @property
    def image_url(self):
        if self.icon and hasattr(self.icon, 'url'):
            return self.icon.url

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cms_reward'

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from cloudinary.models import CloudinaryField
from ..accounts.models import Account
from ..users.models import User


class ProductOffering(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    photo = CloudinaryField('photo')
    name = models.CharField(max_length=200)
    volume = models.CharField(
        choices=settings.PRODUCT_OFFERINGS_VOLUME_TYPES,
        default='700mL',
        max_length=10)
    price = models.DecimalField(default=0, max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])
    author = models.ForeignKey(User, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    is_type = models.CharField(default='Promo', max_length=50)

    def __str__(self):
        return self.product_name
    
    class Meta:
        db_table = 'cms_product_offering'
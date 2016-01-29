from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from cloudinary.models import CloudinaryField


class Contest(models.Model):
    name = models.CharField(max_length=200)
    publish_duration_date_start = models.DateTimeField(null=True, blank=True)
    publish_duration_date_end = models.DateTimeField(null=True, blank=True)
    banner = CloudinaryField('banner')
    points = models.PositiveSmallIntegerField(default=0, blank=False, validators=[MinValueValidator(0)])
    author = models.ForeignKey('myuser.myuser', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    is_type = models.CharField(default='Contest', max_length=50)
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    category = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        default='contests')
    question_title = models.TextField(max_length=300, null=True)

    def publish(self):
        self.publish_schedule = timezone.now()
        self.save()

    @property
    def image_url(self):
        if self.banner and hasattr(self.banner, 'url'):
            return self.banner.url

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Contests'
        db_table = 'cms_contest'

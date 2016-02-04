from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django import forms
from .models import ProductOffering
from cloudinary.forms import CloudinaryFileField
import cloudinary


class CustomCloudinaryField(CloudinaryFileField):
    my_default_error_messages = {
        'required': _("No file selected!")
    }
    default_error_messages = forms.FileField.default_error_messages.copy()
    default_error_messages.update(my_default_error_messages)
    def __init__(self, options=None, autosave=True, *args, **kwargs):
        self.autosave = autosave
        self.options = options or {}
        super(CustomCloudinaryField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        value = super(CloudinaryFileField, self).to_python(value)
        if not value:
            return None
        file_spec = value
        filename = "media/uploads/%s" % 'test_this_tempfile'
        fout = open(filename, 'wb')
        for chunk in file_spec.chunks():
            fout.write(chunk)
        fout.close()
        import magic
        f = magic.Magic(mime=True, uncompress=True)
        # f.from_file('testdata/test.gz')
        file_type = f.from_file(filename).decode("utf-8")[:5]
        if file_type != 'image':
            error_msg = 'Must be a valid image file type.'
            raise ValidationError(_('Invalid file type'), code='invalid')
        else:
            if not value:
                return None
            if self.autosave:
                return cloudinary.uploader.upload_image(value, **self.options)
            else:
                return value


class Product_Offerings_Form(forms.ModelForm):
    photo = CustomCloudinaryField(
        options = {
          'crop': 'limit',
          'width': '740',
          'height': '480',
          'format': 'png',
          'quality': '80',
          'tags': ['product_offerings',]
        },
      )

    class Meta:
        model = ProductOffering
        fields = ('photo', 'name', 'volume', 'price', 'is_featured',)


    def clean(self):
          cleaned_data = super(Product_Offerings_Form, self).clean()
          price = cleaned_data.get("price")
          try:
            if price < 0:
              error_msg = "Price must be a positive number"
              # raise forms.ValidationError(error_msg)
              self.add_error('price', error_msg)
          except:
            pass
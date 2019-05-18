from django import forms
from .models import Image
from django.utils.text import slugify
from urllib import request
from django.core.files.base import ContentFile


class ImageCreateForm(forms.ModelForm):

    # We define because we have to download image first
    def save(self, commit=True):
        image = super(ImageCreateForm, self).save(commit)
        image_url = self.cleaned_data['url']
        image_name = '{} {}'.format(slugify(image.title),image_url.rsplit('.', 1)[1].lower())

        # download image from give url
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)

        if commit:
            image.save(True)
        return image

    class Meta:
            model = Image
            fields = ['title', 'url', 'description']
            widgets = {
                'url': forms.HiddenInput,
            }


    # Validation for url field
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url


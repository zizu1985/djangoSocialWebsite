from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.urlresolvers import reverse

" Represent simple image uploaded by user "
class Image(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created_by')
    title = models.CharField(max_length=200, default="Image")
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True,db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="images_liked", blank=True)

    def __str__(self):
        return self.title

    # Generate slug if somebody missed this
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('image:detail', args=[self.id, self.slug])

    @property
    def get_absolute_image_url(self):
        return "http://127.0.0.1:8000/{0}".format(self.image.url)
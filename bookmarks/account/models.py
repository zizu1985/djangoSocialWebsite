from django.conf.project_template.project_name import settings
from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Profile extends User from authorization model by adding 2 fields
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d',blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    @property
    def get_absolute_image_url(self):
        return "http://127.0.0.1:8000/{0}".format(self.photo.url)


# SQL command
class SQLCommand(models.Model):
    # TODO - jak zrobic relacja do tabeli USER, tak aby klucz obcy nie byl UNIQUE
    #user = models.ManyToManyRel(to=settings.AUTH_USER_MODEL,field="id")
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,null=True)
    approved = models.BooleanField(default=False)
    creation_date = models.DateField(blank=True, null=True)
    approved_date = models.DateField(blank=True, null=True)
    command = models.CharField(max_length=255)

    def set_approved(self, approved):
        self.approved = approved

    def set_creation_date(self, cdate):
        self.creation_date = cdate

    def set_user(self, user):
        self.user = user

    def __str__(self):
        return 'SQL command to execute is {}'.format(self.command)




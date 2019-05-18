# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0003_auto_20190505_1336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sqlcommand',
            name='user',
        ),
        migrations.AddField(
            model_name='sqlcommand',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='user',
        ),
        migrations.RemoveField(
            model_name='image',
            name='users_like',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]

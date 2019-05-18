# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_sqlcommand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sqlcommand',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sqlcommand',
            name='approved_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sqlcommand',
            name='command',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='sqlcommand',
            name='creation_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]

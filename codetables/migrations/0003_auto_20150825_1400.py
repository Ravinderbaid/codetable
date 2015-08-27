# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('codetables', '0002_remove_file_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='author',
            field=models.ForeignKey(verbose_name=b'by', to=settings.AUTH_USER_MODEL),
        ),
    ]

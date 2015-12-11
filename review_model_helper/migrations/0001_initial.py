# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.CharField(serialize=False, primary_key=True, max_length=10)),
                ('title', models.CharField(blank=True, null=True, max_length=100)),
                ('description', models.CharField(blank=True, null=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='ProductReviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('review_text', models.CharField(max_length=1000)),
                ('product_id', models.ForeignKey(to='review_model_helper.Product')),
            ],
        ),
    ]

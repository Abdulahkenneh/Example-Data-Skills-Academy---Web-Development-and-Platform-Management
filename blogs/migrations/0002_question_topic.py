# Generated by Django 5.0.6 on 2024-07-28 14:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='topic',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='blogs.coursetopic'),
            preserve_default=False,
        ),
    ]

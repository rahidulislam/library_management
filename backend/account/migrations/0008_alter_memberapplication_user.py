# Generated by Django 5.0.7 on 2024-08-12 09:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_memberapplication_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberapplication',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='member_application', to=settings.AUTH_USER_MODEL),
        ),
    ]

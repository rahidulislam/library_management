# Generated by Django 5.0.7 on 2024-08-12 08:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberapplication',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='member_application', to='account.profile'),
        ),
    ]

# Generated by Django 5.0.7 on 2024-08-25 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0004_subscriptionplan_library_branch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='library_branch',
        ),
    ]
# Generated by Django 5.0.7 on 2024-08-12 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_rename_feedback_memberapplication_reject_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberapplication',
            name='birth_registration',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='memberapplication',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='memberapplication',
            name='nid',
            field=models.CharField(blank=True, max_length=17, null=True, unique=True),
        ),
    ]

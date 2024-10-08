# Generated by Django 5.0.7 on 2024-08-14 12:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_member_library_branch'),
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='library_branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='library.librarybranch'),
            preserve_default=False,
        ),
    ]

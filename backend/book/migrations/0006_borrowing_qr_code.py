# Generated by Django 5.0.7 on 2024-08-28 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_borrowing_borrow_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowing',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/'),
        ),
    ]

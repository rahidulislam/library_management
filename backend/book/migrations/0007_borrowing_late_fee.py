# Generated by Django 5.0.7 on 2024-09-22 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_borrowing_qr_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowing',
            name='late_fee',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]

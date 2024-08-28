# Generated by Django 5.0.7 on 2024-08-28 09:16

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_remove_book_available_copies_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowing',
            name='borrow_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
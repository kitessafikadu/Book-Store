# Generated by Django 3.2 on 2024-12-25 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0007_remove_user_is_librarian'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_user',
            field=models.BooleanField(default=True),
        ),
    ]
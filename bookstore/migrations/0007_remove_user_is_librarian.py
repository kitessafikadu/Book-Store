# Generated by Django 3.2 on 2024-12-25 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0006_rename_is_publisher_user_is_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_librarian',
        ),
    ]
# Generated by Django 3.2 on 2024-12-25 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0005_feedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_publisher',
            new_name='is_user',
        ),
    ]
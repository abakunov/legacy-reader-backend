# Generated by Django 3.2.3 on 2021-07-18 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20210703_1730'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chapter',
            old_name='number_in_book',
            new_name='index',
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='text',
        ),
    ]
# Generated by Django 3.1.7 on 2021-05-26 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_auto_20210526_1232'),
        ('contenttypes', '0002_remove_content_type_name'),

    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='Comment',
            new_name='comment',
        ),
    ]

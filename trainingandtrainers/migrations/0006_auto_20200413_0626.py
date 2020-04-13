# Generated by Django 2.2.12 on 2020-04-13 06:26

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('wagtailmenus', '0023_remove_use_specific'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('trainingandtrainers', '0005_homepage'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HomePage',
            new_name='Home',
        ),
    ]

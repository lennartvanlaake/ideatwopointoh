# Generated by Django 3.0.5 on 2020-04-07 18:16

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('trainingandtrainers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ideatraining',
            name='demo',
            field=wagtail.core.fields.StreamField([('choice', wagtail.core.blocks.ChoiceBlock(choices=[('tea', 'Tea'), ('coffee', 'Coffee')], icon='cup'))], null=True),
        ),
    ]

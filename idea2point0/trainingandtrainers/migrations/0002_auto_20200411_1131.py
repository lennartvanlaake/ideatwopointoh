# Generated by Django 2.2.12 on 2020-04-11 11:31

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('trainingandtrainers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('profilePicture', models.ImageField(upload_to='trainers/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png,'])])),
                ('name', models.CharField(default='', max_length=100)),
                ('age', models.IntegerField(default=0)),
                ('city', models.CharField(default='', max_length=100)),
                ('country', models.CharField(default='', max_length=100)),
                ('shortBio', models.CharField(default='', max_length=3000)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='TrainingEvent',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('Title', models.CharField(max_length=100)),
                ('date', models.DateTimeField(verbose_name='date and time of event')),
                ('street', models.CharField(default='', max_length=100, verbose_name='Street and number')),
                ('city', models.CharField(default='', max_length=100)),
                ('country', models.CharField(default='', max_length=100)),
                ('contactemail', models.CharField(blank=True, max_length=100, verbose_name='Contact Emailadresss')),
                ('contactwebsite', models.CharField(blank=True, max_length=100, verbose_name='Contact website')),
                ('description', models.CharField(default='', max_length=3000)),
                ('trainer1', models.CharField(default='', max_length=100)),
                ('trainer2', models.CharField(blank=True, max_length=100)),
                ('trainer3', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.RemoveField(
            model_name='ideatraining',
            name='body',
        ),
        migrations.RemoveField(
            model_name='ideatraining',
            name='demo',
        ),
        migrations.RemoveField(
            model_name='ideatraining',
            name='doekmans',
        ),
        migrations.RemoveField(
            model_name='ideatraining',
            name='intro',
        ),
        migrations.AddField(
            model_name='ideatraining',
            name='category',
            field=models.CharField(choices=[('Training', 'Training'), ('Debate', 'Debate Content'), ('Pedagogy', 'Pedagogy Content')], default='', max_length=250),
        ),
        migrations.AddField(
            model_name='ideatraining',
            name='language',
            field=models.CharField(choices=[('English', 'English'), ('Dutch', 'Dutch'), ('German', 'German'), ('Slovak', 'Slovak'), ('Estionian', 'Estonian'), ('Latvian', 'Latvian'), ('Romanian', 'Romanian'), ('Macedonian', 'Macedonian')], default='', max_length=250),
        ),
        migrations.AddField(
            model_name='ideatraining',
            name='level',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='', max_length=250),
        ),
        migrations.AddField(
            model_name='ideatraining',
            name='subject',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='ideatraining',
            name='summary',
            field=models.CharField(default='', max_length=3000),
        ),
        migrations.AddField(
            model_name='ideatraining',
            name='targetAudience',
            field=models.CharField(choices=[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior'), ('GR', 'Graduate')], default='', max_length=250),
        ),
        migrations.AddField(
            model_name='ideatraining',
            name='training',
            field=models.FileField(blank=True, upload_to='trainings/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
        migrations.AlterField(
            model_name='ideatraining',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='Training created'),
        ),
    ]

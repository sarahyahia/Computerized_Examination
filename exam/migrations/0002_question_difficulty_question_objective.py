# Generated by Django 4.0 on 2021-12-30 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='difficulty',
            field=models.IntegerField(choices=[(1, 'simple'), (2, 'difficult')], default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='objective',
            field=models.IntegerField(choices=[(1, 'reminding'), (2, 'understanding'), (3, 'creativity')], default=1),
            preserve_default=False,
        ),
    ]

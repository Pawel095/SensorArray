# Generated by Django 3.0.5 on 2020-05-07 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200504_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='loggeddata',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

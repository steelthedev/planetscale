# Generated by Django 4.0.5 on 2022-07-06 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='created_on',
            field=models.DateField(auto_now_add=True),
        ),
    ]
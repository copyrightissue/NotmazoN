# Generated by Django 4.0.8 on 2022-11-08 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemsforsale', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]

# Generated by Django 4.2.11 on 2024-03-04 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolioApi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialplatformsmodel',
            name='featured',
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]

# Generated by Django 4.2.11 on 2024-03-05 07:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolioApi', '0004_resumeuploadmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='EducationInfoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(max_length=255)),
                ('university', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('university_logo', models.ImageField(blank=True, upload_to='university_logo/')),
                ('cgpa', models.DecimalField(blank=True, decimal_places=2, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10.0)])),
                ('featured', models.BooleanField(db_index=True, default=True)),
            ],
        ),
    ]

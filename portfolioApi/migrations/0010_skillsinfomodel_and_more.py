# Generated by Django 4.2.11 on 2024-03-06 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolioApi', '0009_certificateinfomodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkillsInfoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=100)),
                ('years_of_exp', models.IntegerField(default=0)),
                ('skill_badge', models.ImageField(blank=True, upload_to='skills_badge/')),
            ],
        ),
        migrations.AlterField(
            model_name='certificateinfomodel',
            name='course_badge',
            field=models.ImageField(blank=True, upload_to='certificates_badge/'),
        ),
        migrations.AlterField(
            model_name='educationinfomodel',
            name='university_logo',
            field=models.ImageField(blank=True, upload_to='universities_logo/'),
        ),
    ]
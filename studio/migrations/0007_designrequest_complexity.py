# Generated by Django 5.1.3 on 2024-11-12 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0006_loginattempt'),
    ]

    operations = [
        migrations.AddField(
            model_name='designrequest',
            name='complexity',
            field=models.IntegerField(default=0),
        ),
    ]
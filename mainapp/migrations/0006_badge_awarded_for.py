# Generated by Django 5.0.3 on 2024-04-24 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_achievement_badge'),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='awarded_for',
            field=models.CharField(default='Comment', max_length=50),
        ),
    ]
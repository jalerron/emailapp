# Generated by Django 4.2 on 2024-02-08 09:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_mailings_frequency_alter_mailings_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailings',
            name='end_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='время окончания рассылки'),
        ),
    ]

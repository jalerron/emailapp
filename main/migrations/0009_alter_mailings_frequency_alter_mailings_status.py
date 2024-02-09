# Generated by Django 4.2 on 2024-02-08 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_logs_message_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailings',
            name='frequency',
            field=models.CharField(choices=[('Ежедневно', 'DAILY'), ('Еженедельно', 'WEEKLY'), ('Ежемесячно', 'MONTHLY')], default='Ежедневно', max_length=20, verbose_name='частота'),
        ),
        migrations.AlterField(
            model_name='mailings',
            name='status',
            field=models.CharField(blank=True, choices=[('Выполнена', 'COMPLETED'), ('Создана', 'CREATED'), ('В работе', 'LAUNCHED')], default='Создана', null=True, verbose_name='статус рассылки'),
        ),
    ]

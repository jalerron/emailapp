# Generated by Django 4.2 on 2024-02-04 03:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='почта')),
                ('first_name', models.CharField(max_length=100, verbose_name='имя')),
                ('middle_name', models.CharField(max_length=100, verbose_name='отчество')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='фамилия')),
                ('comments', models.TextField(blank=True, max_length=400, null=True, verbose_name='комментарий')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
        migrations.CreateModel(
            name='Mailings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='название')),
                ('content', models.TextField(verbose_name='контент')),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='время начала рассылки')),
                ('end_time', models.DateTimeField(verbose_name='время окончания рассылки')),
                ('frequency', models.CharField(choices=[('daily', 'раз в день'), ('weekly', 'раз в неделю'), ('monthly', 'раз в месяц')], default='daily', max_length=20, verbose_name='частота')),
                ('status', models.CharField(choices=[('created', 'Создана'), ('started', 'Запущена'), ('completed', 'Завершена')], default='created', max_length=20, verbose_name='статус рассылки')),
                ('clients', models.ManyToManyField(to='main.client', verbose_name='клиенты')),
            ],
            options={
                'verbose_name': 'рассылка',
                'verbose_name_plural': 'рассылки',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=100, verbose_name='тема')),
                ('body', models.TextField(max_length=400, verbose_name='тело письма')),
                ('mailings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.mailings', verbose_name='рассылка')),
            ],
            options={
                'verbose_name': 'сообщение',
                'verbose_name_plural': 'сообщения',
            },
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='время')),
                ('status', models.CharField(max_length=50, verbose_name='статус')),
                ('response', models.TextField(blank=True, verbose_name='ответ')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.message', verbose_name='сообщение')),
            ],
            options={
                'verbose_name': 'логи',
                'verbose_name_plural': 'логи',
            },
        ),
    ]

from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='почта')
    first_name = models.CharField(max_length=100, verbose_name='имя')
    middle_name = models.CharField(max_length=100, verbose_name='отчество')
    last_name = models.CharField(max_length=100, verbose_name='фамилия', **NULLABLE)
    comments = models.TextField(max_length=400, verbose_name='комментарий', **NULLABLE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Mailings(models.Model):

    PERIODICITY_CHOICES = [
        ('daily', 'раз в день'),
        ('weekly', 'раз в неделю'),
        ('monthly', 'раз в месяц'),
    ]

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    title = models.CharField(max_length=255, verbose_name='название')
    content = models.TextField(verbose_name='контент')
    clients = models.ManyToManyField(Client, verbose_name='клиенты')
    start_time = models.DateTimeField(default=timezone.now, verbose_name='время начала рассылки')
    end_time = models.DateTimeField(verbose_name='время окончания рассылки')
    frequency = models.CharField(choices=PERIODICITY_CHOICES, default='daily', max_length=20, verbose_name='частота')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', verbose_name='статус рассылки')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Message(models.Model):
    mailings = models.ForeignKey(Mailings, on_delete=models.CASCADE, verbose_name='рассылка')
    topic = models.CharField(max_length=100, verbose_name='тема')
    body = models.TextField(max_length=400, verbose_name='тело письма')

    def __str__(self):
        return f'{self.mailings} - {self.topic}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Logs(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение')
    time = models.DateTimeField(default=timezone.now, verbose_name='время')
    status = models.CharField(max_length=50, verbose_name='статус')
    response = models.TextField(blank=True, verbose_name='ответ')

    def __str__(self):
        return f'{self.message} - {self.status}'

    class Meta:
        verbose_name = 'логи'
        verbose_name_plural = 'логи'

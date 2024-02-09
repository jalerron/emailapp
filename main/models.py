from django.db import models
from django.utils import timezone

from emailapp import settings

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='почта')
    first_name = models.CharField(max_length=100, verbose_name='имя')
    middle_name = models.CharField(max_length=100, verbose_name='отчество')
    last_name = models.CharField(max_length=100, verbose_name='фамилия', **NULLABLE)
    comments = models.TextField(max_length=400, verbose_name='комментарий', **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):

    topic = models.CharField(max_length=100, verbose_name='тема')
    body = models.TextField(max_length=400, verbose_name='тело письма')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.topic}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailings(models.Model):
    class Periodicity(models.TextChoices):
        DAILY = 'Ежедневно', 'DAILY'
        WEEKLY = 'Еженедельно', 'WEEKLY'
        MONTHLY = 'Ежемесячно', 'MONTHLY'

    class SendStatus(models.TextChoices):
        COMPLETED = 'Выполнена', 'COMPLETED'
        CREATED = 'Создана', 'CREATED'
        LAUNCHED = 'В работе', 'LAUNCHED'

    title = models.CharField(max_length=255, verbose_name='название')
    content = models.TextField(verbose_name='контент')
    clients = models.ManyToManyField(Client, verbose_name='клиенты')
    start_time = models.DateTimeField(default=timezone.now, verbose_name='время начала рассылки')
    end_time = models.DateTimeField(default=timezone.now, verbose_name='время окончания рассылки')
    frequency = models.CharField(choices=Periodicity.choices, default=Periodicity.DAILY, max_length=20,
                                 verbose_name='частота')
    status = models.CharField(choices=SendStatus.choices, default=SendStatus.CREATED, verbose_name='статус рассылки', **NULLABLE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, default=1, verbose_name='cообщение')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='активность')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

        permissions = [
            ('set_active',
             'может менять состояние активности')
        ]


class Logs(models.Model):
    class LogStatus(models.TextChoices):
        OK = 'Успешно', 'Successfully'
        FAILED = 'Неудачно', 'Failed'
        UNKNOWN = 'Неизвестно', 'Unknown'

    message_title = models.ForeignKey(Mailings, on_delete=models.CASCADE, verbose_name='сообщение')
    time = models.DateTimeField(default=timezone.now, verbose_name='время')
    status = models.CharField(choices=LogStatus.choices, default=LogStatus.UNKNOWN, verbose_name='статус')
    response = models.TextField(blank=True, verbose_name='ответ')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.message_title} - {self.status}'

    class Meta:
        verbose_name = 'логи'
        verbose_name_plural = 'логи'

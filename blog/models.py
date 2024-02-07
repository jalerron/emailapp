from django.db import models


NULLABLE = {'null': True, 'blank': True}


class Blog(models.Model):

    title = models.CharField(max_length=100, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержимое')
    image = models.ImageField(upload_to='blog/%Y/%m/%d', verbose_name='изображение', **NULLABLE)
    views_count = models.SmallIntegerField(default=0, verbose_name='Количество просмотров')
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return f'{self.title} | {self.date_published} | {self.views_count}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
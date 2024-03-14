from django.db import models


class Cat(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя котика')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='media/cat_images/', verbose_name='Изображение котика')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Котик'
        verbose_name_plural = 'Котики'



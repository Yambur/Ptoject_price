from django.db import models
from django.core.exceptions import ValidationError

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    """" Модель продукта """
    title = models.CharField(max_length=100, verbose_name='Наименование')
    model = models.CharField(max_length=100, verbose_name='Модель')
    date = models.DateField(verbose_name='Дата выхода на рынок')

    def __str__(self):
        return f'{self.title}, {self.model} ({self.date})'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Contact(models.Model):
    """" Модель контактов """
    email = models.EmailField(max_length=254, verbose_name='E-mail')
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    h_number = models.PositiveIntegerField(verbose_name='Номер дома')

    def __str__(self):
        return f'{self.email} ({self.country}, {self.city}, {self.street}. {self.h_number})'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Seller(models.Model):
    """" Модель звена торговой сети """
    SELLER_TYPES = [
        (0, 'Завод'),
        (1, 'Розничная сеть'),
        (2, 'Индивидуальный предприниматель')
    ]
    seller_type = models.PositiveIntegerField(choices=SELLER_TYPES, verbose_name='Тип')
    title = models.CharField(max_length=100, verbose_name='Наименование')
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, verbose_name='Контакты')
    product = models.ManyToManyField('Product', verbose_name='Продукты')
    supplier = models.ForeignKey('Seller', on_delete=models.PROTECT, verbose_name='Поставщик', **NULLABLE)
    level = models.PositiveIntegerField(verbose_name='Уровень')
    debt = models.FloatField(verbose_name='Задолженность перед поставщиком', **NULLABLE)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')

    def __str__(self):
        return f'{self.seller_type} {self.title} (создано {self.created})'

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if self.seller_type == 0 and self.level != 0:
            raise ValidationError('У завода может быть только уровень 0!')
        if self.seller_type != 0 and self.level == 0:
            raise ValidationError('Уровень 0 может быть только у завода!')
        # любой объект, кроме завода, должен иметь поставщика
        if self.seller_type != 0 and self.supplier == None:
            raise ValidationError('Укажите поставщика!')
        if self.supplier and self.level != (self.supplier.level + 1):
            raise ValidationError('Уровень объекта должен быть на 1 выше, чем уровень поставщика')
        # у завода не может быть задолженности перед поставщиком
        if self.seller_type == 0 and self.debt != None:
            raise ValidationError('У завода не может быть задолженности перед поставщиком')
        if self.debt < 0:
            raise ValidationError('Сумма задолженности должна быть положительным числом')

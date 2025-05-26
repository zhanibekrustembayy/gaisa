from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from django.core.files.storage import default_storage as storage  

from django.contrib.auth.models import User

import math

# Модели отображают информацию о данных, с которыми вы работаете.
# Они содержат поля и поведение ваших данных.
# Обычно одна модель представляет одну таблицу в базе данных.
# Каждая модель это класс унаследованный от django.db.models.Model.
# Атрибут модели представляет поле в базе данных.
# Django предоставляет автоматически созданное API для доступа к данным

# choices (список выбора). Итератор (например, список или кортеж) 2-х элементных кортежей,
# определяющих варианты значений для поля.
# При определении, виджет формы использует select вместо стандартного текстового поля
# и ограничит значение поля указанными значениями.

# Читабельное имя поля (метка, label). Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField,
# первым аргументом принимает необязательное читабельное название.
# Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.
# null - Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.
# blank - Если True, поле не обязательно и может быть пустым. По умолчанию - False.
# Это не то же что и null. null относится к базе данных, blank - к проверке данных.
# Если поле содержит blank=True, форма позволит передать пустое значение.
# При blank=False - поле обязательно.

# Объект строительства
class Construction(models.Model):
    title = models.CharField(_('construction_title'), max_length=256)
    details = models.TextField(_('construction_details'))
    address = models.CharField(_('address'), max_length=256)
    customer = models.CharField(_('customer'), max_length=256)
    completion = models.CharField(_('completion'), max_length=64)
    price = models.DecimalField(_('price'), max_digits=15, decimal_places=2)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'construction'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['title']),
        ]
        # Сортировка по умолчанию
        ordering = ['title']
    def __str__(self):
        # Вывод в тег SELECT 
        return "{}".format(self.address)

# Инвесторы
class Investor(models.Model):
    fio = models.CharField(_('fio'), max_length=256)
    email = models.EmailField(_('email'))
    phone = models.CharField(_('phone'), max_length=64)
    link = models.URLField(max_length=200, blank=True, null=True)
    photo = models.ImageField(_('investor_photo'), upload_to='images/', blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'investor'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['fio']),
        ]
        # Сортировка по умолчанию
        ordering = ['fio']
    def __str__(self):
        # Вывод в тег SELECT 
        return "{}, {}".format(self.fio, self.phone)

# Привязка объектов к инвесторам
class Binding(models.Model):
    construction = models.ForeignKey(Construction, related_name='binding_construction', on_delete=models.CASCADE)
    investor = models.ForeignKey(Investor, related_name='binding_investor', on_delete=models.CASCADE)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'binding'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['construction']),
            models.Index(fields=['investor']),
        ]
        # Сортировка по умолчанию
        #ordering = ['fio']
    def __str__(self):
        # Вывод в тег SELECT 
        return "{}. {}".format(self.construction, self.investor)

# Инвестиции
class Investments(models.Model):
    datein = models.DateTimeField(_('datein'))
    construction = models.ForeignKey(Construction, related_name='investments_construction', on_delete=models.CASCADE)
    investor = models.ForeignKey(Investor, related_name='investments_investor', on_delete=models.CASCADE)
    amount = models.DecimalField(_('amount'), max_digits=15, decimal_places=2)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'investments'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['construction']),
            models.Index(fields=['investor']),
        ]
        # Сортировка по умолчанию
        #ordering = ['fio']
    def __str__(self):
        # Вывод в тег SELECT 
        return "{}. {}. {}".format(self.construction, self.investor, self.amount)

# Приходные накладные 
class Coming(models.Model):
    organization = models.CharField(_('organization'), max_length=256)
    datec = models.DateTimeField(_('datec'))
    numb = models.IntegerField(_('numb'))     
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'coming'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['datec']),            
        ]
        # Сортировка по умолчанию
        ordering = ['datec']
    def __str__(self):
        # Вывод названия в тег SELECT 
        return "#{} {}".format(self.numb, self.datec)

# Категория товара
class Category(models.Model):
    title = models.CharField(_('category_title'), max_length=128, unique=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'category'
    def __str__(self):
        # Вывод названияв тег SELECT 
        return "{}".format(self.title)

# Каталог товаров
class Catalog(models.Model):
    coming = models.ForeignKey(Coming, related_name='catalog_coming', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='catalog_category', on_delete=models.CASCADE)
    title = models.CharField(_('catalog_title'), max_length=255)
    details = models.TextField(_('catalog_details'), blank=True, null=True)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    quantity = models.IntegerField(_('quantity'))
    unit = models.CharField(_('unit'), max_length=32)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'catalog'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['title']),
        ]
        # Сортировка по умолчанию
        ordering = ['title']
    def __str__(self):
        # Вывод в тег SELECT 
        return "{} {} {}".format(self.category, self.title, self.price)

# Представление базы данных Каталог товаров (со средней оценкой)
class ViewCatalog(models.Model):
    category_id = models.IntegerField(_('category_id'))
    category = models.CharField(_('category_title'), max_length=128)
    title = models.CharField(_('catalog_title'), max_length=255)
    details = models.TextField(_('catalog_details'), blank=True, null=True)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    quantity = models.IntegerField(_('quantity'))
    unit = models.CharField(_('unit'), max_length=32)
    sale_quantity = models.IntegerField(_('sale_quantity'))
    available = models.IntegerField(_('available'))
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'view_catalog'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['title']),
        ]
        # Сортировка по умолчанию
        ordering = ['title']
        # Таблицу не надо не добавлять не удалять
        managed = False
    def __str__(self):
        # Вывод в тег SELECT 
        return "{} {} {}".format(self.category, self.title, self.price)
    
# Расходные накладные 
class Outgo(models.Model):
    construction = models.ForeignKey(Construction, related_name='outgo_construction', on_delete=models.CASCADE)
    dateo = models.DateTimeField(_('dateo'))
    numb = models.IntegerField(_('numb'))     
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'outgo'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['construction']),            
            models.Index(fields=['dateo']),            
        ]
        # Сортировка по умолчанию
        ordering = ['dateo']
    def __str__(self):
        # Вывод названия в тег SELECT 
        return "#{} {}".format(self.numb, self.dateo)
        # Override the save method of the model

# Продажа 
class Sale(models.Model):
    outgo = models.ForeignKey(Outgo, related_name='sale_outgo', on_delete=models.CASCADE)
    catalog = models.ForeignKey(Catalog, related_name='sale_catalog', on_delete=models.CASCADE)
    quantity = models.IntegerField(_('quantity'), default=1)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'sale'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['outgo']),
            models.Index(fields=['catalog']),
        ]
        # Сортировка по умолчанию
        ordering = ['outgo']
    # Сумма по товару
    def total(self):
        return self.price * self.quantity
    def __str__(self):
        # Вывод в тег SELECT 
        return "{}: {}".format(self.catalog, self.quantity)
        # Таблицу не надо не добавлять не удалять
        #managed = False

# Новости 
class News(models.Model):
    daten = models.DateTimeField(_('daten'))
    title = models.CharField(_('title_news'), max_length=256)
    details = models.TextField(_('details_news'))
    photo = models.ImageField(_('photo_news'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'news'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['daten']),
        ]
        # Сортировка по умолчанию
        ordering = ['daten']
    #def save(self):
    #    super().save()
    #    img = Image.open(self.photo.path) # Open image
    #    # resize image
    #    if img.width > 512 or img.height > 700:
    #        proportion_w_h = img.width/img.height  # Отношение ширины к высоте 
    #        output_size = (512, int(512/proportion_w_h))
    #        img.thumbnail(output_size) # Изменение размера
    #        img.save(self.photo.path) # Сохранение

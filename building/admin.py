from django.contrib import admin

# Register your models here.
from .models import Construction, Investor, Binding, Investments, Coming, Category, Catalog, Outgo, Sale, News

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Construction)
admin.site.register(Investor)
admin.site.register(Binding)
admin.site.register(Investments)
admin.site.register(Coming)
admin.site.register(Category)
admin.site.register(Catalog)
admin.site.register(Outgo)
admin.site.register(Sale)
admin.site.register(News)

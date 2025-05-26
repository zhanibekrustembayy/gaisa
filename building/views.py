from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.urls import reverse

from django.contrib.auth import login as auth_login

import datetime

import time

import csv
import xlwt
from io import BytesIO

# Подключение моделей
from django.contrib.auth.models import User, Group

from django.db import models
from django.db.models import Q

from .models import Construction, Investor, Binding, Investments, Coming, Category, Catalog, ViewCatalog, Outgo, Sale, News
# Подключение форм
from .forms import ConstructionForm, InvestorForm, BindingForm, InvestmentsForm, ComingForm, CategoryForm, CatalogForm, OutgoForm, SaleForm, NewsForm, SignUpForm

from django.contrib.auth.models import AnonymousUser

# Create your views here.
# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

# Стартовая страница 
def index(request):
    news1 = News.objects.all().order_by('-daten')[0:1]
    news24 = News.objects.all().order_by('-daten')[1:4]
    construction = Construction.objects.order_by('?')[0:4]
    return render(request, "index.html", {"news1": news1, "news24": news24 , "construction": construction ,})    

# Контакты
def contact(request):
    return render(request, "contact.html")

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def construction_index(request):
    construction = Construction.objects.all().order_by('title')
    return render(request, "construction/index.html", {"construction": construction,})

# Список 
def construction_list(request):
    construction = Construction.objects.all().order_by('title')
    return render(request, "construction/list.html", {"construction": construction,})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на коре# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def construction_create(request):
    try:
        if request.method == "POST":
            construction = Construction()
            construction.title = request.POST.get("title")
            construction.details = request.POST.get("details")
            construction.address = request.POST.get("address")
            construction.customer = request.POST.get("customer")
            construction.completion = request.POST.get("completion")
            construction.price = request.POST.get("price")
            constructionform = ConstructionForm(request.POST)
            if constructionform.is_valid():
                construction.save()
                return HttpResponseRedirect(reverse('construction_index'))
            else:
                return render(request, "construction/create.html", {"form": constructionform})
        else:        
            constructionform = ConstructionForm()
            return render(request, "construction/create.html", {"form": constructionform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def construction_edit(request, id):
    try:
        construction = Construction.objects.get(id=id)
        if request.method == "POST":
            construction.title = request.POST.get("title")
            construction.details = request.POST.get("details")
            construction.address = request.POST.get("address")
            construction.customer = request.POST.get("customer")
            construction.completion = request.POST.get("completion")
            construction.price = request.POST.get("price")
            constructionform = ConstructionForm(request.POST)
            if constructionform.is_valid():
                construction.save()
                return HttpResponseRedirect(reverse('construction_index'))
            else:
                return render(request, "construction/edit.html", {"form": constructionform})
        else:
            # Загрузка начальных данных
            constructionform = ConstructionForm(initial={'title': construction.title, 'details': construction.details, 'address': construction.address, 'customer': construction.customer, 'completion': construction.completion, 'price': construction.price, })
            return render(request, "construction/edit.html", {"form": constructionform})
    except Construction.DoesNotExist:
        return HttpResponseNotFound("<h2>Construction not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def construction_delete(request, id):
    try:
        construction = Construction.objects.get(id=id)
        construction.delete()
        return HttpResponseRedirect(reverse('construction_index'))
    except Construction.DoesNotExist:
        return HttpResponseNotFound("<h2>Construction not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def construction_read(request, id):
    try:
        construction = Construction.objects.get(id=id) 
        return render(request, "construction/read.html", {"construction": construction})
    except Construction.DoesNotExist:
        return HttpResponseNotFound("<h2>Construction not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)


# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def investor_index(request):
    #investor = Investor.objects.all().order_by('surname', 'name', 'patronymic')
    #return render(request, "investor/index.html", {"investor": investor})
    investor = Investor.objects.all().order_by('fio')
    return render(request, "investor/index.html", {"investor": investor})

# Список для просмотра
def investor_list(request):
    investor = Investor.objects.all().order_by('fio')
    return render(request, "investor/list.html", {"investor": investor})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def investor_create(request):
    if request.method == "POST":
        investor = Investor()        
        investor.fio = request.POST.get("fio")
        investor.email = request.POST.get("email")
        investor.phone = request.POST.get("phone")
        investor.link = request.POST.get("link")
        if 'photo' in request.FILES:                
            investor.photo = request.FILES['photo']        
        investor.save()
        return HttpResponseRedirect(reverse('investor_index'))
    else:        
        #investorform = InvestorForm(request.FILES, initial={'daten': datetime.datetime.now().strftime('%Y-%m-%d'),})
        investorform = InvestorForm()
        return render(request, "investor/create.html", {"form": investorform})

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def investor_edit(request, id):
    try:
        investor = Investor.objects.get(id=id) 
        if request.method == "POST":
            investor.fio = request.POST.get("fio")
            investor.email = request.POST.get("email")
            investor.phone = request.POST.get("phone")
            investor.link = request.POST.get("link")
            if "photo" in request.FILES:                
                investor.photo = request.FILES["photo"]
            investor.save()
            return HttpResponseRedirect(reverse('investor_index'))
        else:
            # Загрузка начальных данных
            investorform = InvestorForm(initial={'fio': investor.fio, 'email': investor.email, 'phone': investor.phone, 'link': investor.link, 'photo': investor.photo })
            return render(request, "investor/edit.html", {"form": investorform})
    except Investor.DoesNotExist:
        return HttpResponseNotFound("<h2>Investor not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def investor_delete(request, id):
    try:
        investor = Investor.objects.get(id=id)
        investor.delete()
        return HttpResponseRedirect(reverse('investor_index'))
    except Investor.DoesNotExist:
        return HttpResponseNotFound("<h2>Investor not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
@login_required
def investor_read(request, id):
    try:
        investor = Investor.objects.get(id=id) 
        return render(request, "investor/read.html", {"investor": investor})
    except Investor.DoesNotExist:
        return HttpResponseNotFound("<h2>Investor not found</h2>")

@login_required
@group_required("Managers")
def binding_index(request):
    binding = Binding.objects.all().order_by('construction')
    return render(request, "binding/index.html", {"binding": binding,})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на коре# Список для изменения с кнопками создать, изменить, удалить

@login_required
@group_required("Managers")
def binding_create(request):
    try:
        if request.method == "POST":
            binding = Binding()
            binding.construction = Construction.objects.filter(id=request.POST.get("construction")).first()
            binding.investor = Investor.objects.filter(id=request.POST.get("investor")).first()            
            bindingform = BindingForm(request.POST)
            if bindingform.is_valid():
                binding.save()
                return HttpResponseRedirect(reverse('binding_index'))
            else:
                return render(request, "binding/create.html", {"form": bindingform})
        else:        
            bindingform = BindingForm()
            return render(request, "binding/create.html", {"form": bindingform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def binding_edit(request, id):
    try:
        binding = Binding.objects.get(id=id)
        if request.method == "POST":
            binding.construction = Construction.objects.filter(id=request.POST.get("construction")).first()
            binding.investor = Investor.objects.filter(id=request.POST.get("investor")).first()    
            bindingform = BindingForm(request.POST)
            if bindingform.is_valid():
                binding.save()
                return HttpResponseRedirect(reverse('binding_index'))
            else:
                return render(request, "binding/edit.html", {"form": bindingform})
        else:
            # Загрузка начальных данных
            bindingform = BindingForm(initial={'construction': binding.construction, 'investor': binding.investor, })
            return render(request, "binding/edit.html", {"form": bindingform})
    except Binding.DoesNotExist:
        return HttpResponseNotFound("<h2>Binding not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def binding_delete(request, id):
    try:
        binding = Binding.objects.get(id=id)
        binding.delete()
        return HttpResponseRedirect(reverse('binding_index'))
    except Binding.DoesNotExist:
        return HttpResponseNotFound("<h2>Binding not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def binding_read(request, id):
    try:
        binding = Binding.objects.get(id=id) 
        return render(request, "binding/read.html", {"binding": binding})
    except Binding.DoesNotExist:
        return HttpResponseNotFound("<h2>Binding not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

@login_required
@group_required("Managers")
def investments_index(request):
    investments = Investments.objects.all().order_by('construction')
    return render(request, "investments/index.html", {"investments": investments,})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на коре# Список для изменения с кнопками создать, изменить, удалить

@login_required
@group_required("Managers")
def investments_create(request):
    try:
        if request.method == "POST":
            investments = Investments()
            investments.datein = request.POST.get("datein")
            investments.construction = Construction.objects.filter(id=request.POST.get("construction")).first()
            investments.investor = Investor.objects.filter(id=request.POST.get("investor")).first() 
            investments.amount = request.POST.get("amount")
            investmentsform = InvestmentsForm(request.POST)
            if investmentsform.is_valid():
                investments.save()
                return HttpResponseRedirect(reverse('investments_index'))
            else:
                return render(request, "investments/create.html", {"form": investmentsform})
        else:        
            investmentsform = InvestmentsForm(initial={'datein': datetime.datetime.now().strftime('%Y-%m-%d'), })
            return render(request, "investments/create.html", {"form": investmentsform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def investments_edit(request, id):
    try:
        investments = Investments.objects.get(id=id)
        if request.method == "POST":
            investments.datein = request.POST.get("datein")
            investments.construction = Construction.objects.filter(id=request.POST.get("construction")).first()
            investments.investor = Investor.objects.filter(id=request.POST.get("investor")).first() 
            investments.amount = request.POST.get("amount")   
            investmentsform = InvestmentsForm(request.POST)
            if investmentsform.is_valid():
                investments.save()
                return HttpResponseRedirect(reverse('investments_index'))
            else:
                return render(request, "investments/edit.html", {"form": investmentsform})
        else:
            # Загрузка начальных данных
            investmentsform = InvestmentsForm(initial={'datein': investments.datein.strftime('%Y-%m-%d'), 'construction': investments.construction,  'investor': investments.investor,  'amount': investments.amount, })
            return render(request, "investments/edit.html", {"form": investmentsform})
    except Investments.DoesNotExist:
        return HttpResponseNotFound("<h2>Investments not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def investments_delete(request, id):
    try:
        investments = Investments.objects.get(id=id)
        investments.delete()
        return HttpResponseRedirect(reverse('investments_index'))
    except Investments.DoesNotExist:
        return HttpResponseNotFound("<h2>Investments not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def investments_read(request, id):
    try:
        investments = Investments.objects.get(id=id) 
        return render(request, "investments/read.html", {"investments": investments})
    except Investments.DoesNotExist:
        return HttpResponseNotFound("<h2>Investments not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

@login_required
@group_required("Managers")
def coming_index(request):
    coming = Coming.objects.all().order_by('datec')
    return render(request, "coming/index.html", {"coming": coming,})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на коре# Список для изменения с кнопками создать, изменить, удалить

@login_required
@group_required("Managers")
def coming_create(request):
    try:
        if request.method == "POST":
            coming = Coming()
            coming.organization = request.POST.get("organization")
            coming.datec = request.POST.get("datec")
            coming.numb = request.POST.get("numb")
            comingform = ComingForm(request.POST)
            if comingform.is_valid():
                coming.save()
                return HttpResponseRedirect(reverse('coming_index'))
            else:
                return render(request, "coming/create.html", {"form": comingform})
        else:        
            comingform = ComingForm(initial={'datec': datetime.datetime.now().strftime('%Y-%m-%d'), })
            return render(request, "coming/create.html", {"form": comingform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def coming_edit(request, id):
    try:
        coming = Coming.objects.get(id=id)
        if request.method == "POST":
            coming.organization = request.POST.get("organization")
            coming.datec = request.POST.get("datec")
            coming.numb = request.POST.get("numb")   
            comingform = ComingForm(request.POST)
            if comingform.is_valid():
                coming.save()
                return HttpResponseRedirect(reverse('coming_index'))
            else:
                return render(request, "coming/edit.html", {"form": comingform})
        else:
            # Загрузка начальных данных
            comingform = ComingForm(initial={'datec': coming.datec.strftime('%Y-%m-%d'), 'organization': coming.organization,  'numb': coming.numb, })
            return render(request, "coming/edit.html", {"form": comingform})
    except Coming.DoesNotExist:
        return HttpResponseNotFound("<h2>Coming not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def coming_delete(request, id):
    try:
        coming = Coming.objects.get(id=id)
        coming.delete()
        return HttpResponseRedirect(reverse('coming_index'))
    except Coming.DoesNotExist:
        return HttpResponseNotFound("<h2>Coming not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def coming_read(request, id):
    try:
        coming = Coming.objects.get(id=id) 
        return render(request, "coming/read.html", {"coming": coming})
    except Coming.DoesNotExist:
        return HttpResponseNotFound("<h2>Coming not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def category_index(request):
    category = Category.objects.all().order_by('title')
    return render(request, "category/index.html", {"category": category,})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def category_create(request):
    try:
        if request.method == "POST":
            category = Category()
            category.title = request.POST.get("title")
            categoryform = CategoryForm(request.POST)
            if categoryform.is_valid():
                category.save()
                return HttpResponseRedirect(reverse('category_index'))
            else:
                return render(request, "category/create.html", {"form": categoryform})
        else:        
            categoryform = CategoryForm()
            return render(request, "category/create.html", {"form": categoryform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def category_edit(request, id):
    try:
        category = Category.objects.get(id=id)
        if request.method == "POST":
            category.title = request.POST.get("title")
            categoryform = CategoryForm(request.POST)
            if categoryform.is_valid():
                category.save()
                return HttpResponseRedirect(reverse('category_index'))
            else:
                return render(request, "category/edit.html", {"form": categoryform})
        else:
            # Загрузка начальных данных
            categoryform = CategoryForm(initial={'title': category.title, })
            return render(request, "category/edit.html", {"form": categoryform})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def category_delete(request, id):
    try:
        category = Category.objects.get(id=id)
        category.delete()
        return HttpResponseRedirect(reverse('category_index'))
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def category_read(request, id):
    try:
        category = Category.objects.get(id=id) 
        return render(request, "category/read.html", {"category": category})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def catalog_index(request, coming_id):
    #catalog = Catalog.objects.all().order_by('title')
    coming = Coming.objects.get(id=coming_id)
    catalog = Catalog.objects.filter(coming_id=coming_id).order_by('title')
    return render(request, "catalog/index.html", {"catalog": catalog, "coming": coming, "coming_id": coming_id})
    
# Список для просмотра и отправки в корзину
@login_required
@group_required("Managers")
#@login_required
def catalog_list(request):
    try:
        # Только доступный товар
        catalog = Catalog.objects.order_by('title').order_by('category')
        catalog = ViewCatalog.objects.filter(available__gt=0).order_by('title').order_by('category')
#        catalog = Catalog.objects.raw("""
#SELECT catalog.id, catalog.category_id, category.title AS category, catalog.title,catalog.details, catalog.price, catalog.quantity, catalog.unit, 
#(SELECT SUM(quantity) FROM sale WHERE sale.catalog_id = catalog.id) AS sale_quantity,
#IIF ((catalog.quantity - (SELECT SUM(quantity) FROM sale WHERE sale.catalog_id = catalog.id)) IS NULL, catalog.quantity, (catalog.quantity - (SELECT SUM(quantity) FROM sale WHERE sale.catalog_id = catalog.id)) ) AS available
#FROM catalog LEFT JOIN category ON catalog.category_id = category.id
#WHERE catalog.quantity > %d
#ORDER BY catalog.title,  catalog.title
#""",  params=[0])
        print(catalog)        
        return render(request, "catalog/list.html", {"catalog": catalog })           
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def catalog_create(request, coming_id):
    try:
        if request.method == "POST":
            catalog = Catalog()
            catalog.coming_id = coming_id
            catalog.category = Category.objects.filter(id=request.POST.get("category")).first()
            catalog.title = request.POST.get("title")
            catalog.details = request.POST.get("details")        
            catalog.price = request.POST.get("price")
            catalog.quantity = request.POST.get("quantity")
            catalog.unit = request.POST.get("unit")
            catalogform = CatalogForm(request.POST)
            if catalogform.is_valid():
                catalog.save()
                return HttpResponseRedirect(reverse('catalog_index', args=(coming_id,)))
            else:
                return render(request, "catalog/create.html", {"form": catalogform})
        else:        
            catalogform = CatalogForm()
            return render(request, "catalog/create.html", {"form": catalogform, "coming_id": coming_id})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def catalog_edit(request, id, coming_id):
    try:
        catalog = Catalog.objects.get(id=id) 
        if request.method == "POST":
            catalog.category = Category.objects.filter(id=request.POST.get("category")).first()
            catalog.title = request.POST.get("title")
            catalog.details = request.POST.get("details")        
            catalog.price = request.POST.get("price")
            catalog.quantity = request.POST.get("quantity")
            catalog.unit = request.POST.get("unit")
            catalogform = CatalogForm(request.POST)
            if catalogform.is_valid():
                catalog.save()
                return HttpResponseRedirect(reverse('catalog_index', args=(coming_id,)))
            else:
                return render(request, "catalog/edit.html", {"form": catalogform, "coming_id": coming_id})            
        else:
            # Загрузка начальных данных
            catalogform = CatalogForm(initial={'category': catalog.category, 'title': catalog.title, 'details': catalog.details, 'price': catalog.price, 'quantity': catalog.quantity, 'unit': catalog.unit, })
            #print('->',catalog.photo )
            return render(request, "catalog/edit.html", {"form": catalogform, "coming_id": coming_id})
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def catalog_delete(request, id, coming_id):
    try:
        catalog = Catalog.objects.get(id=id)
        catalog.delete()
        return HttpResponseRedirect(reverse('catalog_index', args=(coming_id,)))
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы с информацией о товаре для менеджера.
@login_required
@group_required("Managers")
def catalog_read(request, id, coming_id):
    try:
        catalog = Catalog.objects.get(id=id) 
        return render(request, "catalog/read.html", {"catalog": catalog, "coming_id": coming_id})
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы с информацией о товаре для клиента
#@login_required
def catalog_details(request, id):
    try:
        # Товар с каталога
        catalog = ViewCatalog.objects.get(id=id)
        # Отзывы на данный товар
        #reviews = ViewSale.objects.filter(catalog_id=id).exclude(rating=None)
        return render(request, "catalog/details.html", {"catalog": catalog,})
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")

@login_required
@group_required("Managers")
def outgo_index(request):
    outgo = Outgo.objects.all().order_by('dateo')
    return render(request, "outgo/index.html", {"outgo": outgo,})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на коре# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def outgo_create(request):
    try:
        if request.method == "POST":
            outgo = Outgo()
            outgo.construction = Construction.objects.filter(id=request.POST.get("construction")).first()
            outgo.dateo = request.POST.get("dateo")
            outgo.numb = request.POST.get("numb")
            outgoform = OutgoForm(request.POST)
            if outgoform.is_valid():
                outgo.save()
                return HttpResponseRedirect(reverse('outgo_index'))
            else:
                return render(request, "outgo/create.html", {"form": outgoform})
        else:        
            outgoform = OutgoForm(initial={'dateo': datetime.datetime.now().strftime('%Y-%m-%d'), })
            return render(request, "outgo/create.html", {"form": outgoform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def outgo_edit(request, id):
    try:
        outgo = Outgo.objects.get(id=id)
        if request.method == "POST":
            outgo.construction = Construction.objects.filter(id=request.POST.get("construction")).first()
            outgo.dateo = request.POST.get("dateo")
            outgo.numb = request.POST.get("numb")   
            outgoform = OutgoForm(request.POST)
            if outgoform.is_valid():
                outgo.save()
                return HttpResponseRedirect(reverse('outgo_index'))
            else:
                return render(request, "outgo/edit.html", {"form": outgoform})
        else:
            # Загрузка начальных данных
            outgoform = OutgoForm(initial={'dateo': outgo.dateo.strftime('%Y-%m-%d'), 'construction': outgo.construction,  'numb': outgo.numb, })
            return render(request, "outgo/edit.html", {"form": outgoform})
    except Outgo.DoesNotExist:
        return HttpResponseNotFound("<h2>Outgo not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def outgo_delete(request, id):
    try:
        outgo = Outgo.objects.get(id=id)
        outgo.delete()
        return HttpResponseRedirect(reverse('outgo_index'))
    except Outgo.DoesNotExist:
        return HttpResponseNotFound("<h2>Outgo not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def outgo_read(request, id):
    try:
        outgo = Outgo.objects.get(id=id) 
        return render(request, "outgo/read.html", {"outgo": outgo})
    except Outgo.DoesNotExist:
        return HttpResponseNotFound("<h2>Outgo not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

    # Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def sale_index(request, outgo_id):
    #sale = Sale.objects.all()
    outgo = Outgo.objects.get(id=outgo_id)
    sale = Sale.objects.filter(outgo_id=outgo_id)
    return render(request, "sale/index.html", {"sale": sale, "outgo": outgo, "outgo_id": outgo_id})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def sale_create(request, outgo_id):
    try:
        if request.method == "POST":
            sale = Sale()
            sale.outgo_id = outgo_id
            sale.catalog = Catalog.objects.filter(id=request.POST.get("catalog")).first()
            #sale.catalog = ViewCatalog.objects.filter(id=request.POST.get("catalog")).first()
            sale.quantity = request.POST.get("quantity")
            saleform = SaleForm(request.POST)
            if saleform.is_valid():
                sale.save()
                return HttpResponseRedirect(reverse('sale_index', args=(outgo_id,)))
            else:
                return render(request, "sale/create.html", {"form": saleform})
        else:        
            saleform = SaleForm()
            return render(request, "sale/create.html", {"form": saleform, "outgo_id": outgo_id})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def sale_edit(request, id, outgo_id):
    try:
        sale = Sale.objects.get(id=id) 
        if request.method == "POST":
            sale.catalog = Catalog.objects.filter(id=request.POST.get("catalog")).first()
            sale.quantity = request.POST.get("quantity")
            saleform = SaleForm(request.POST)
            if saleform.is_valid():
                sale.save()
                return HttpResponseRedirect(reverse('sale_index', args=(outgo_id,)))
            else:
                return render(request, "sale/edit.html", {"form": saleform, "outgo_id": outgo_id})            
        else:
            # Загрузка начальных данных
            saleform = SaleForm(initial={'catalog': sale.catalog, 'quantity': sale.quantity, })
            #print('->',sale.photo )
            return render(request, "sale/edit.html", {"form": saleform, "outgo_id": outgo_id})
    except Sale.DoesNotExist:
        return HttpResponseNotFound("<h2>Sale not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def sale_delete(request, id, outgo_id):
    try:
        sale = Sale.objects.get(id=id)
        sale.delete()
        return HttpResponseRedirect(reverse('sale_index', args=(outgo_id,)))
    except Sale.DoesNotExist:
        return HttpResponseNotFound("<h2>Sale not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы с информацией о товаре для менеджера.
@login_required
@group_required("Managers")
def sale_read(request, id, outgo_id):
    try:
        sale = Sale.objects.get(id=id) 
        return render(request, "sale/read.html", {"sale": sale, "outgo_id": outgo_id})
    except Sale.DoesNotExist:
        return HttpResponseNotFound("<h2>Sale not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def news_index(request):
    #news = News.objects.all().order_by('surname', 'name', 'patronymic')
    #return render(request, "news/index.html", {"news": news})
    news = News.objects.all().order_by('-daten')
    return render(request, "news/index.html", {"news": news})

# Список для просмотра
def news_list(request):
    news = News.objects.all().order_by('-daten')
    return render(request, "news/list.html", {"news": news})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def news_create(request):
    if request.method == "POST":
        news = News()        
        news.daten = request.POST.get("daten")
        news.title = request.POST.get("title")
        news.details = request.POST.get("details")
        if 'photo' in request.FILES:                
            news.photo = request.FILES['photo']        
        news.save()
        return HttpResponseRedirect(reverse('news_index'))
    else:        
        #newsform = NewsForm(request.FILES, initial={'daten': datetime.datetime.now().strftime('%Y-%m-%d'),})
        newsform = NewsForm(initial={'daten': datetime.datetime.now().strftime('%Y-%m-%d'), })
        return render(request, "news/create.html", {"form": newsform})

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def news_edit(request, id):
    try:
        news = News.objects.get(id=id) 
        if request.method == "POST":
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if "photo" in request.FILES:                
                news.photo = request.FILES["photo"]
            news.save()
            return HttpResponseRedirect(reverse('news_index'))
        else:
            # Загрузка начальных данных
            newsform = NewsForm(initial={'daten': news.daten.strftime('%Y-%m-%d'), 'title': news.title, 'details': news.details, 'photo': news.photo })
            return render(request, "news/edit.html", {"form": newsform})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def news_delete(request, id):
    try:
        news = News.objects.get(id=id)
        news.delete()
        return HttpResponseRedirect(reverse('news_index'))
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")

# Просмотр страницы read.html для просмотра объекта.
#@login_required
def news_read(request, id):
    try:
        news = News.objects.get(id=id) 
        return render(request, "news/read.html", {"news": news})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")

# Экспорт в Excel
def export_excel(request): 
    # Create a HttpResponse object and set its content_type header value to Microsoft excel.
    response = HttpResponse(content_type='application/vnd.ms-excel') 
    # Set HTTP response Content-Disposition header value. Tell web server client the attached file name is students.xls.
    response['Content-Disposition'] = 'attachment;filename=catalog.xls' 
    # Create a new Workbook file.
    work_book = xlwt.Workbook(encoding = 'utf-8') 
    # Create a new worksheet in the above workbook.
    work_sheet = work_book.add_sheet(u'Catalog Info')
    # Maintain some worksheet styles，style_head_row, style_data_row, style_green, style_red
    # This style will be applied to worksheet head row.
    style_head_row = xlwt.easyxf("""    
        align:
          wrap off,
          vert center,
          horiz center;
        borders:
          left THIN,
          right THIN,
          top THIN,
          bottom THIN;
        font:
          name Arial,
          colour_index white,
          bold on,
          height 0xA0;
        pattern:
          pattern solid,
          fore-colour 0x19;
        """
    )
    # Define worksheet data row style. 
    style_data_row = xlwt.easyxf("""
        align:
          wrap on,
          vert center,
          horiz left;
        font:
          name Arial,
          bold off,
          height 0XA0;
        borders:
          left THIN,
          right THIN,
          top THIN,
          bottom THIN;
        """
    )
    # Set data row date string format.
    #style_data_row.num_format_str = 'dd/mm/yyyy'
    # Define a green color style.
    style_green = xlwt.easyxf(" pattern: fore-colour 0x11, pattern solid;")
    # Define a red color style.
    style_red = xlwt.easyxf(" pattern: fore-colour 0x0A, pattern solid;")
    # Generate worksheet head row data.
    work_sheet.write(0,0, 'category', style_head_row) 
    work_sheet.write(0,1, 'title', style_head_row) 
    work_sheet.write(0,2, 'price', style_head_row) 
    work_sheet.write(0,3, 'available', style_head_row) 
    work_sheet.write(0,4, 'unit', style_head_row) 
    # Generate worksheet data row data.
    row = 1 
    for catalog in ViewCatalog.objects.filter(available__gt=0).order_by('title').order_by('category'):
        work_sheet.write(row,0, catalog.category, style_data_row)
        work_sheet.write(row,1, catalog.title, style_data_row)
        work_sheet.write(row,2, '{:.0f}'.format(catalog.price), style_data_row)
        work_sheet.write(row,3, catalog.available, style_data_row)
        work_sheet.write(row,4, catalog.unit, style_data_row)
        row=row + 1 
    # Create a StringIO object.
    output = BytesIO()
    
    # Save the workbook data to the above StringIO object.
    work_book.save(output)
    # Reposition to the beginning of the StringIO object.
    output.seek(0)
    # Write the StringIO object's value to HTTP response to send the excel file to the web server client.
    response.write(output.getvalue()) 
    return response

# Регистрационная форма 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return HttpResponseRedirect(reverse('index'))
            #return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Изменение данных пользователя
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('index')
    #success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user




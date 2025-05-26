from datetime import datetime
from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, DateTimeInput, NumberInput, CheckboxInput
from .models import Construction, Investor, Binding, Investments, Coming, Category, Catalog, ViewCatalog, Outgo, Sale, News
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

import datetime
from django.utils import timezone

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.

class ConstructionForm(forms.ModelForm):
    class Meta:
        model = Construction
        fields = ['title', 'details', 'address', 'customer', 'completion', 'price']
        widgets = {
            'title': TextInput(attrs={"size":"100"}),        
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),     
            'address': TextInput(attrs={"size":"100"}),      
            'customer': TextInput(attrs={"size":"100"}),      
            'completion': TextInput(attrs={"size":"50"}),      
            'price': NumberInput(attrs={"size":"10"}),
        }
        labels = {
            'title': _('construction_title'),            
            'details': _('construction_details'),            
        }

class InvestorForm(forms.ModelForm):
    class Meta:
        model = Investor
        fields = ('fio', 'email', 'phone', 'link', 'photo')
        widgets = {
            'fio': TextInput(attrs={"size":"100"}),
            'email': TextInput(attrs={"size":"100", "type":"email", "pattern": "[^@\s]+@[^@\s]+\.[^@\s]+"}),
            'phone': TextInput(attrs={"size":"100", "type":"tel", "pattern": "+7-[0-9]{3}-[0-9]{3}-[0-9]{4}"}),
            'link':  TextInput(attrs={"size":"100", "type":"url"}),            
        }

class BindingForm(forms.ModelForm):
    class Meta:
        model = Binding
        fields = ['construction', 'investor']
        widgets = {
            'construction': forms.Select(attrs={'class': 'chosen'}),
            'investor': forms.Select(attrs={'class': 'chosen'}),
        }
        labels = {
            'construction': _('binding_construction'),            
            'investor': _('binding_investor'),            
        }

class InvestmentsForm(forms.ModelForm):
    class Meta:
        model = Investments
        fields = ['datein', 'construction', 'investor', 'amount']
        widgets = {
            'datein': DateTimeInput(format='%d.%m.%Y'), 
            'construction': forms.Select(attrs={'class': 'chosen'}),
            'investor': forms.Select(attrs={'class': 'chosen'}),
            'amount': NumberInput(attrs={"size":"10"}),
        }
        labels = {
            'construction': _('investments_construction'),            
            'investor': _('investments_investor'),            
        }

# Приходные накладные  
class ComingForm(forms.ModelForm):
    class Meta:
        model = Coming
        fields = ('organization', 'datec', 'numb',)
        widgets = {
            'organization': TextInput(attrs={"size":"100"}),
            'datec': DateInput(attrs={"type":"date"}),
            'numb': DateInput(attrs={"type":"number"}),
        }
    # Метод-валидатор для поля datec
    def clean_datec(self):
        data = self.cleaned_data['datec']
        #print(data)
        #print(timezone.now())
        # Проверка даты (не больше текущей даты-времени)
        if data > timezone.now():
            raise forms.ValidationError(_('Cannot be greater than the current date'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data
    # Метод-валидатор для поля numb
    def clean_numb(self):
        data = self.cleaned_data['numb']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('The number must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data        

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title',]
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }
        labels = {
            'title': _('category_title'),            
        }
    # Метод-валидатор для поля title
    #def clean_title(self):
    #    data = self.cleaned_data['title']
    #    # Ошибка если начинается не с большой буквы
    #    if data.istitle() == False:
    #        raise forms.ValidationError(_('Value must start with a capital letter'))
    #    # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
    #    return data

class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ('category', 'title', 'details', 'price', 'quantity', 'unit')
        widgets = {
            'category': forms.Select(attrs={'class': 'chosen'}),
            'title': TextInput(attrs={"size":"50"}),
            'details': Textarea(attrs={'cols': 50, 'rows': 5}),            
            'price': NumberInput(attrs={"size":"10"}),
            'quantity': NumberInput(attrs={"size":"10"}),
            'unit': TextInput(attrs={"size":"50"}),
        }
        labels = {
            'category': _('category'),            
        }
    # Метод-валидатор для поля numb
    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('Quantity must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data
    # Метод-валидатор для поля price
    def clean_price(self):
        data = self.cleaned_data['price']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('Price must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data        

# Приходные накладные  
class OutgoForm(forms.ModelForm):
    class Meta:
        model = Outgo
        fields = ('construction', 'dateo', 'numb',)
        widgets = {
            'construction': forms.Select(attrs={'class': 'chosen'}),
            'dateo': DateInput(attrs={"type":"date"}),
            'numb': DateInput(attrs={"type":"number"}),
        }
        labels = {
            'construction': _('construction'),            
        }
    # Метод-валидатор для поля dateo
    def clean_dateo(self):
        data = self.cleaned_data['dateo']
        #print(data)
        #print(timezone.now())
        # Проверка даты (не больше текущей даты-времени)
        if data > timezone.now():
            raise forms.ValidationError(_('Cannot be greater than the current date'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data
    # Метод-валидатор для поля numb
    def clean_numb(self):
        data = self.cleaned_data['numb']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('The number must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data        

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('catalog', 'quantity')
        widgets = {
            'catalog': forms.Select(attrs={'class': 'chosen'}),
            'quantity': NumberInput(attrs={"size":"10"}),            
        }
        labels = {
            'catalog': _('catalog'),            
        }
    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        available = ViewCatalog.objects.filter(available__gt=0).only('id').all()
        self.fields['catalog'].queryset = Catalog.objects.filter(id__in = available)
    # Метод-валидатор для поля numb
    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('Quantity must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('daten', 'title', 'details', 'photo')
        widgets = {
            'dater': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }
    # Метод-валидатор для поля daten
    def clean_daten(self):        
        if isinstance(self.cleaned_data['daten'], datetime) == True:
            data = self.cleaned_data['daten']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data    

# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')
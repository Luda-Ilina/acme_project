# birthday/views.py
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import BirthdayForm
from .models import Birthday
# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown

# Создаём миксин.
# class BirthdayMixin:
#     model = Birthday
#     form_class = BirthdayForm
#     template_name = 'birthday/birthday.html'
#     success_url = reverse_lazy('birthday:list')


# class BirthdayMixin:
#     model = Birthday
#     success_url = reverse_lazy('birthday:list')


# class BirthdayFormMixin:
#     form_class = BirthdayForm
#     template_name = 'birthday/birthday.html'


# Наследуем класс от встроенного ListView:
class BirthdayListView(ListView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = 'id'
    # ...и даже настройки пагинации:
    paginate_by = 10


# # Добавляем миксин первым по списку родительских классов.
# class BirthdayCreateView(BirthdayMixin, BirthdayFormMixin, CreateView):
#     # Не нужно описывать атрибуты: все они унаследованы от BirthdayMixin.
#     form_class = BirthdayForm


# class BirthdayUpdateView(BirthdayMixin, BirthdayFormMixin, UpdateView):
#     # И здесь все атрибуты наследуются от BirthdayMixin.
#     form_class = BirthdayForm


# class BirthdayDeleteView(BirthdayMixin, DeleteView):
#     pass


class BirthdayCreateView(CreateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayUpdateView(UpdateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayDeleteView(DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')


# class BirthdayCreateView(CreateView):
#     # Указываем модель, с которой работает CBV...
#     model = Birthday

#     # Этот класс сам может создать форму на основе модели!
#     # Нет необходимости отдельно создавать форму через ModelForm.
#     # Указываем поля, которые должны быть в форме:
#     # fields = '__all__'

#     # Класс CreateView может использовать форму,
#     # созданную отдельно через класс ModelForm.
#     # Применим эту возможность и
#     # подключим форму BirthdayForm к классу BirthdayCreateView:
#     # для этого вместо атрибута fields нужно указать атрибут form_class;
#     # значением этого атрибута будет BirthdayForm.
#     # Указываем имя формы:
#     form_class = BirthdayForm

#     # Явным образом указываем шаблон:
#     template_name = 'birthday/birthday.html'

#     # Указываем namespace:name страницы, куда будет перенаправлен пользователь
#     # после создания объекта:
#     success_url = reverse_lazy('birthday:list')


# class BirthdayUpdateView(UpdateView):
#     model = Birthday
#     form_class = BirthdayForm
#     template_name = 'birthday/birthday.html'
#     success_url = reverse_lazy('birthday:list')


# class BirthdayDeleteView(DeleteView):
#     model = Birthday
#     success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(DetailView):
    model = Birthday

    # Переопределяем словарь контекста, чтобы подключить функцию подсчета дней.
    def get_context_data(self, **kwargs):
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context

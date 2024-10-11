# birthday/views.py

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import BirthdayForm, CongratulationForm
from .models import Birthday, Congratulation
# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown


# Будут обработаны POST-запросы только от залогиненных пользователей.
@login_required
def add_comment(request, pk):
    # Получаем объект дня рождения или выбрасываем 404 ошибку.
    birthday = get_object_or_404(Birthday, pk=pk)
    # Функция должна обрабатывать только POST-запросы.
    form = CongratulationForm(request.POST)
    if form.is_valid():
        # Создаём объект поздравления, но не сохраняем его в БД.
        congratulation = form.save(commit=False)
        # В поле author передаём объект автора поздравления.
        congratulation.author = request.user
        # В поле birthday передаём объект дня рождения.
        congratulation.birthday = birthday
        # Сохраняем объект в БД.
        congratulation.save()
    # Перенаправляем пользователя назад, на страницу дня рождения.
    return redirect('birthday:detail', pk=pk)


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

class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


# Наследуем класс от встроенного ListView:
class BirthdayListView(ListView):
    # Указываем модель, с которой работает CBV...
    model = Birthday
    # По умолчанию этот класс выполняет запрос
    # queryset = Birthday.objects.all(),
    # но мы его переопределим м добавим запрос к объектам,
    # связанным с Birthday через поле author.
    queryset = Birthday.objects.prefetch_related('tags'
                                                 ).select_related('author')
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


class BirthdayCreateView(LoginRequiredMixin, CreateView):
    model = Birthday
    form_class = BirthdayForm

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)


class BirthdayUpdateView(OnlyAuthorMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayDeleteView(OnlyAuthorMixin, DeleteView):
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

#     # Указываем namespace:name страницы, куда будет перенаправлен
#     # пользователь после создания объекта:
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
        # Записываем в переменную form пустой объект формы.
        context['form'] = CongratulationForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
        )
        # Возвращаем словарь контекста.
        return context

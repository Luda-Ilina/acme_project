# from django.shortcuts import render

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
# from .forms import BirthdayForm

# Исходный вид
# def birthday(request):
#     context = {}
#     return render(request, 'birthday/birthday.html', context=context)


# Стало:
# def birthday(request):
#     # Если есть GET-параметры — передаём их в форму:
#     form = BirthdayForm(request.GET or None)
#     if form.is_valid():
#         pass
#     print(request.GET)
#     # Добавляем его в словарь контекста под ключом form:
#     # Форму с переданным в неё объектом request.GET
#     # записываем в словарь контекста...
#     context = {'form': form}
#     # Указываем нужный шаблон и передаём в него словарь контекста.
#     return render(request, 'birthday/birthday.html', context)


from django.shortcuts import get_object_or_404, redirect, render

from .forms import BirthdayForm
from .models import Birthday
# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown

# Вызовем функцию calculate_birthday_countdown() из view-функции birthday().
# Чтобы передать в функцию calculate_birthday_countdown()
# дату рождения именно как дату (а не как строку),
# значение даты нужно взять из словаря form.cleaned_data,
# в котором содержатся валидированные данные, приведённые к нужным типам.
# Дата дня рождения в этом словаре доступна через
# выражение form.cleaned_data['birthday'];
# тип данных у этого объекта — datetime.date, а не просто строка. То, что надо.


# def edit_birthday(request, pk):
#     # Находим запрошенный объект для редактирования по первичному ключу
#     # или возвращаем 404 ошибку, если такого объекта нет.
#     instance = get_object_or_404(Birthday, pk=pk)
#     # Связываем форму с найденным объектом: передаём его в аргумент instance.
#     form = BirthdayForm(request.POST or None, instance=instance)
#     # Всё остальное без изменений.
#     context = {'form': form}
#     # Сохраняем данные, полученные из формы, и отправляем ответ:
#     if form.is_valid():
#         form.save()
#         birthday_countdown = calculate_birthday_countdown(
#             form.cleaned_data['birthday']
#         )
#         context.update({'birthday_countdown': birthday_countdown})
#     return render(request, 'birthday/birthday.html', context)


# def birthday(request):
#     form = BirthdayForm(request.POST or None)
#     # Создаём словарь контекста сразу после инициализации формы.
#     context = {'form': form}
#     # Если форма валидна...
#     if form.is_valid():
#         # ... сохраним данные из формы в БД
#         form.save()
#         # ...вызовем функцию подсчёта дней:
#         birthday_countdown = calculate_birthday_countdown(
#             # ...и передаём в неё дату из словаря cleaned_data.
#             form.cleaned_data['birthday']
#         )
#         # Обновляем словарь контекста: добавляем в него новый элемент.
#         context.update({'birthday_countdown': birthday_countdown})
#     return render(request, 'birthday/birthday.html', context)


# При этом варианте во view-функциях edit_birthday() и birthday()
# будет много повторяющегося кода.
# Лучше объединить создание и редактирование объекта в одной функции.

# Добавим опциональный параметр pk.
def birthday(request, pk=None):
    # Если в запросе указан pk (если получен запрос на редактирование объекта):
    if pk is not None:
        # Получаем объект модели или выбрасываем 404 ошибку.
        instance = get_object_or_404(Birthday, pk=pk)
    # Если в запросе не указан pk
    # (если получен запрос к странице создания записи):
    else:
        # Связывать форму с объектом не нужно, установим значение None.
        instance = None
    # Передаём в форму либо данные из запроса, либо None.
    # В случае редактирования прикрепляем объект модели.
    form = BirthdayForm(request.POST or None, instance=instance)
    # Остальной код без изменений.
    context = {'form': form}
    # Сохраняем данные, полученные из формы, и отправляем ответ:
    if form.is_valid():
        form.save()
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']
        )
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)


def birthday_list(request):
    # Получаем все объекты модели Birthday из БД.
    birthdays = Birthday.objects.all()
    # Передаём их в контекст шаблона.
    context = {'birthdays': birthdays}
    return render(request, 'birthday/birthday_list.html', context)


def delete_birthday(request, pk):
    # Получаем объект модели или выбрасываем 404 ошибку.
    instance = get_object_or_404(Birthday, pk=pk)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    # Если был получен POST-запрос...
    if request.method == 'POST':
        # ...удаляем объект:
        instance.delete()
        # ...и переадресовываем пользователя на страницу со списком записей.
        return redirect('birthday:list')
    # Если был получен GET-запрос — отображаем форму.
    return render(request, 'birthday/birthday.html', context)
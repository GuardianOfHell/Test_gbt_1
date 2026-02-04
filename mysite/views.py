from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *
from django.shortcuts import render, get_object_or_404
from django.db.models import F


# from mysite.models import News_list, Services_and_Price_menu, Services_and_Price_menu_list_item

def index(request):
    try:
        page = int(request.GET.get('page'))
    except:
        page = None
    print(page)
    if page == None:
        page = 1
    title = 'Головна'
    menu = Services_and_Price_menu_list_item.objects.all()
    return render(request, 'mysite/index.html', {'title': title, 'page': page, 'menu': menu})

def contact(request):
    try:
        page = int(request.GET.get('page'))
    except:
        page = None
    print(page)
    if page == None:
        page = 5
    title = 'Контакти'
    return render(request, 'mysite/index.html', {'title': title, 'page': page})

def production(request):
    try:
        page = int(request.GET.get('page'))
    except:
        page = None
    print(page)
    if page == None:
        page = 3
    title = 'Виробництво'
    return render(request, 'mysite/index.html', {'title': title, 'page': page})

def Delivery_and_payment(request):
    try:
        page = int(request.GET.get('page'))
    except:
        page = None
    print(page)
    if page == None:
        page = 4
    title = 'Доставка та оплата'
    return render(request, 'mysite/index.html', {'title': title, 'page': page})

def project(request):
    try:
        page = int(request.GET.get('page'))
    except:
        page = None
    print(page)
    if page == None:
        page = 6
    title = 'Проекти'
    return render(request, 'mysite/index.html', {'title': title, 'page': page})

def catalog(request):
    title = 'Каталог'
    menu = Services_and_Price_menu_list_item.objects.all()
    try:
        page = int(request.GET.get('page'))
    except:
        page = None
    print(page)
    if page == None:
        page = 2
    try:
        which_catalog = int(request.GET.get('which_catalog'))
    except:
        which_catalog = None
    print(which_catalog)
    if which_catalog == None:
        which_catalog = 1
    goods = (
        Services_and_Price_product_item.objects
        .filter(Name_menu__id=which_catalog)
        .order_by(F("priority").asc(nulls_last=True), "id")
    )
    # <-- ДОДАЙ ОЦЕ
    for g in goods:
        g.sizes_list = [s.strip() for s in (g.Size or "").split("|") if s.strip()]
    # <-- /ДОДАЙ
    return render(request, 'mysite/index.html', {'title': title, 'menu': menu, 'which_catalog': int(which_catalog), 'page': page, 'goods': goods})


def Product_card(request):
    # Отримуємо id товару з GET-параметра '?t='
    product_id = request.GET.get('t')

    # Ваша логіка для отримання сторінки
    try:
        page = int(request.GET.get('page'))
    except (ValueError, TypeError):  # Більш надійна перевірка на помилку
        page = 1

    print(page)  # Ваш print для відладки

    # --- Ключова зміна ---
    # Використовуємо get_object_or_404 - це стандартний і найнадійніший
    # спосіб отримати один об'єкт. Він автоматично обробить помилку,
    # якщо товар з таким id не буде знайдено.
    # .prefetch_related('images') - як і раніше, ефективно завантажує
    # всі пов'язані зображення одним запитом.
    goods = get_object_or_404(
        Services_and_Price_product_item.objects.prefetch_related('images'),
        id=product_id
    )

    # Ваша логіка для меню та заголовка
    title = 'Товар'
    menu = Services_and_Price_menu_list_item.objects.all()

    print(goods)  # Ваш print для відладки

    # Формуємо контекст для передачі в шаблон
    context = {
        'title': title,
        'page': page,
        'menu': menu,
        'goods': goods,
    }

    # ЗАЛИШАЄМО ВАШ КОД: рендеримо шаблон index.html
    return render(request, 'mysite/index.html', context)

import logging
from functools import wraps

from django.shortcuts import render, get_object_or_404
from django.db.models import F

from .models import Services_and_Price_menu_list_item, Services_and_Price_product_item


logger = logging.getLogger(__name__)


def with_page(default_page):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            page_param = request.GET.get('page')
            try:
                page = int(page_param) if page_param is not None else default_page
            except (TypeError, ValueError):
                page = default_page
            request.page = page
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator

@with_page(default_page=1)
def index(request):
    title = 'Головна'
    menu = Services_and_Price_menu_list_item.objects.all()
    return render(request, 'mysite/index.html', {'title': title, 'page': request.page, 'menu': menu})

@with_page(default_page=5)
def contact(request):
    title = 'Контакти'
    return render(request, 'mysite/index.html', {'title': title, 'page': request.page})

@with_page(default_page=3)
def production(request):
    title = 'Виробництво'
    return render(request, 'mysite/index.html', {'title': title, 'page': request.page})

@with_page(default_page=4)
def Delivery_and_payment(request):
    title = 'Доставка та оплата'
    return render(request, 'mysite/index.html', {'title': title, 'page': request.page})

@with_page(default_page=6)
def project(request):
    title = 'Проекти'
    return render(request, 'mysite/index.html', {'title': title, 'page': request.page})

@with_page(default_page=2)
def catalog(request):
    title = 'Каталог'
    menu = Services_and_Price_menu_list_item.objects.all()
    try:
        which_catalog = int(request.GET.get('which_catalog'))
    except (TypeError, ValueError):
        which_catalog = None
        logger.warning("Invalid which_catalog parameter: %s", request.GET.get('which_catalog'))
    if which_catalog is None:
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
    return render(
        request,
        'mysite/index.html',
        {
            'title': title,
            'menu': menu,
            'which_catalog': int(which_catalog),
            'page': request.page,
            'goods': goods,
        },
    )


@with_page(default_page=1)
def Product_card(request):
    # Отримуємо id товару з GET-параметра '?t='
    product_id = request.GET.get('t')

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

    # Формуємо контекст для передачі в шаблон
    context = {
        'title': title,
        'page': request.page,
        'menu': menu,
        'goods': goods,
    }

    # ЗАЛИШАЄМО ВАШ КОД: рендеримо шаблон index.html
    return render(request, 'mysite/index.html', context)

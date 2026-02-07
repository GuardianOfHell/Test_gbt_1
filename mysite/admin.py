# from django.contrib import admin
# from mysite.models import *
#
# class Services_and_Price_menu_list_item_Admin(admin.ModelAdmin):
#     list_display = ('id', 'Title',)
#     list_display_links = ('id', 'Title',)
# admin.site.register(Services_and_Price_menu_list_item, Services_and_Price_menu_list_item_Admin)
#
# class Services_and_Price_product_item_Admin(admin.ModelAdmin):
#     list_display = ('id', 'Title', 'Name_menu')
#     list_display_links = ('id', 'Title', 'Name_menu')
# admin.site.register(Services_and_Price_product_item, Services_and_Price_product_item_Admin)
#
#
from django.contrib import admin
from .models import *
# Додаємо утиліту для відображення HTML в адмін-панелі
from django.utils.html import format_html


# --- Адмін-панель для Категорій меню ---
@admin.register(Services_and_Price_menu_list_item)
class ServicesAndPriceMenuListAdmin(admin.ModelAdmin):
    list_display = ('id', 'Title',)
    list_display_links = ('id', 'Title',)


# --- Адмін-панель для Статусів наявності ---
# Ця модель не була зареєстрована. Додаємо її.
@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'Title',)
    list_display_links = ('id', 'Title',)


# --- Вбудований редактор для зображень товару ---
# Це дозволить додавати багато фото на сторінці одного товару.
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    # Кількість додаткових порожніх слотів для завантаження
    extra = 1
    # Додаємо поле для попереднього перегляду зображення
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        # Перевіряємо, чи існує зображення
        if obj.image:
            return format_html('<a href="{0}" target="_blank"><img src="{0}" width="150" /></a>', obj.image.url)
        return "Немає зображення"
    image_preview.short_description = 'Перегляд'


# --- Основна адмін-панель для Товарів ---
@admin.register(Services_and_Price_product_item)
class ServicesAndPriceProductItemAdmin(admin.ModelAdmin):
    # Додаємо більше полів для відображення у списку
    list_display = ('id', 'Size', 'Title', 'Name_menu', 'price', 'Product_availability')
    list_display_links = ('id', 'Title')
    # Додаємо можливість фільтрації
    list_filter = ('Name_menu', 'Product_availability')
    # Додаємо поле для пошуку
    search_fields = ('Title', 'Product_code')
    # Підключаємо вбудований редактор зображень
    inlines = [ProductImageInline]

# Модель ProductImage не потрібно реєструвати окремо,
# оскільки ми керуємо нею через товар (за допомогою ProductImageInline).
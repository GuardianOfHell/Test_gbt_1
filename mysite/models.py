from django.db import models
import os
from django.db.models import F

class Services_and_Price_menu_list_item(models.Model):
    Title = models.CharField(max_length=244, verbose_name='Назва категорії')
    img = models.FileField(upload_to='Services_and_Price_menu_list_item/', verbose_name='Зображення')

    def delete(self, *args, **kwargs):
        # Удаление изображения, если оно существует
        if self.img:
            try:
                os.remove(self.img.path)  # Удаление файла изображения с диска
            except FileNotFoundError:
                pass  # Если файл уже был удалён, ничего не делать
        super().delete(*args, **kwargs)  # Вызов метода удаления объекта

    def __str__( self ):
        return self.Title

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
        ordering = ['id', 'Title']


class Availability(models.Model):
    Title = models.CharField(max_length=244, verbose_name='Назва наявності')

    class Meta:
        verbose_name = "Наявність"
        verbose_name_plural = "Наявність"

    def __str__(self):
        # Повертає ім'я файлу зображення
        return self.Title

class Services_and_Price_product_item(models.Model):
    Title = models.CharField(max_length=244, verbose_name='Назва товару')
    price = models.CharField(max_length=244, verbose_name='Ціна')
    img = models.FileField(upload_to='Services_and_Price_product_item/', verbose_name='Зображення')
    Name_menu = models.ForeignKey(Services_and_Price_menu_list_item, on_delete=models.PROTECT,
                                  verbose_name='Вибрати пункт в меню')


    Size = models.CharField(max_length=244, verbose_name='Розмір')
    Product_code = models.CharField(max_length=244, verbose_name='Код товару')
    Product_availability = models.ForeignKey(Availability, on_delete=models.PROTECT,
                                  verbose_name='Наявність товару')
    Price_in_detail_o = models.CharField(max_length=244, verbose_name='Ціна детально')
    Price_in_detail_evro = models.CharField(max_length=244, verbose_name='Ціна детально (евро)')
    Characteristics = models.TextField (verbose_name='Характеристики')
    Description = models.TextField (verbose_name='Опис товару')
    priority = models.PositiveIntegerField(null=True, blank=True, db_index=True, verbose_name="Пріоритет")
    def delete(self, *args, **kwargs):
        # Удаление изображения, если оно существует
        if self.img:
            try:
                os.remove(self.img.path)  # Удаление файла изображения с диска
            except FileNotFoundError:
                pass  # Если файл уже был удалён, ничего не делать
        super().delete(*args, **kwargs)  # Вызов метода удаления объекта

    def __str__( self ):
        return self.Title

    class Meta:
        verbose_name = 'Каталог товару'
        verbose_name_plural = 'Каталог товару'
        ordering = [F("priority").asc(nulls_last=True), "id"]


class ProductImage(models.Model):
    """
    Ця модель зберігатиме кожне окреме зображення
    і буде пов'язана з конкретним товаром.
    """
    # ForeignKey створює зв'язок "багато-до-одного".
    # related_name='images' дозволяє звертатися до всіх зображень
    # з об'єкта ProductItem (наприклад, my_product.images.all()).
    # on_delete=models.CASCADE означає, що при видаленні товару
    # всі пов'язані з ним зображення також будуть видалені.
    product = models.ForeignKey(
        Services_and_Price_product_item,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Товар"
    )
    # Поле для зберігання самого зображення.
    image = models.ImageField(
        upload_to='product_images/',
        verbose_name='Зображення'
    )

    class Meta:
        verbose_name = "Зображення товару"
        verbose_name_plural = "Зображення товарів"

    def __str__(self):
        # Повертає ім'я файлу зображення
        return self.image.name
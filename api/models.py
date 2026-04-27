from django.db import models
from django.core.validators import RegexValidator

class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'ch_categories'
        ordering = ['order']
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200, verbose_name='Назва')
    tag = models.CharField(max_length=50, blank=True, verbose_name='Тег')
    description = models.TextField(blank=True, verbose_name='Опис')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Ціна')
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True, verbose_name='Фото')
    is_available = models.BooleanField(default=True, verbose_name='Доступно')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ch_menu_items'
        ordering = ['category', 'name']
        verbose_name = 'Позиція меню'
        verbose_name_plural = 'Позиції меню'

    def __str__(self):
        return f'{self.name} - {self.price} ₴'


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує підтвердження'),
        ('confirmed', 'Підтверджено'),
        ('cancelled', 'Скасовано'),
        ('completed', 'Завершено'),
    ]

    phone_validator = RegexValidator(
        regex=r'^\+?[\d\s\-]{7,15}$',
        message='Невірний формат номера телефону'
    )

    name = models.CharField(max_length=200, verbose_name="Ім'я гостя")
    phone = models.CharField(max_length=20, validators=[phone_validator], verbose_name='Телефон')
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Час')
    guests = models.PositiveSmallIntegerField(default=2, verbose_name='Кількість гостей')
    comment = models.TextField(blank=True, verbose_name='Коментар')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ch_reservations'
        ordering = ['-date', '-time']
        verbose_name = 'Бронювання'
        verbose_name_plural = 'Бронювання'

    def __str__(self):
        return f'{self.name} — {self.date} {self.time} ({self.guests} ос.)'


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новий'),
        ('preparing', 'Готується'),
        ('ready', 'Готовий'),
        ('completed', 'Завершений'),
        ('cancelled', 'Скасовано'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Сума')
    note = models.TextField(blank=True, verbose_name='Примітка')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ch_orders'
        ordering = ['-created_at']
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

    def __str__(self):
        return f'Замовлення #{self.pk} — {self.total_price}'

    def calculate_total(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total_price = total
        self.save(update_fields=['total_price'])
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='Кількість')
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Ціна за одиницю')

    class Meta:
        db_table = 'ch_order_items'
        verbose_name = 'Позиція замовлення'
        verbose_name_plural = 'Позиції замовлення'

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f'{self.menu_item.name} ({self.quantity})'

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    slug = models.SlugField(unique=True, verbose_name="URL")
    icon = models.ImageField(upload_to='icons/', null=True, blank=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name


class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes')
    title = models.CharField(max_length=200, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис", null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ціна")
    weight = models.IntegerField(verbose_name="Вага (г)", default=300)
    image = models.ImageField(upload_to='dishes/', null=True, blank=True)
    is_available = models.BooleanField(default=True, verbose_name="В наявності")
    on_fire = models.BooleanField(default=False, verbose_name="🔥 Smoky Choice")

    class Meta:
        verbose_name = "Страва"
        verbose_name_plural = "Страви"

    def __str__(self):
        return self.title


class Order(models.Model):
    DELIVERY_CHOICES = [
        ('delivery', 'Кур\'єр'),
        ('pickup', 'Самовивіз'),
        ('instore', 'В закладі'),
    ]
    phone_number = models.CharField(max_length=20, verbose_name="Телефон")
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='delivery')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сума (₴)")
    delivery_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    user_coords = models.TextField(verbose_name="Координати", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата замовлення")

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

    def __str__(self):
        return f"Замовлення #{self.id} — {self.phone_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dish_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
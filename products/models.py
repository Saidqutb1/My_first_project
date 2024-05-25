from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name


class MakeCompany(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'makecompany'

    def __str__(self):
        return self.name


class MakeCountry(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'makecountry'

    def __str__(self):
        return self.name


class ProductBatch(models.Model):
    season = models.CharField(max_length=100)

    class Meta:
        db_table = 'productbatch'

    def __str__(self):
        return self.season


class Product(models.Model):
    name = models.CharField(max_length=100)
    body = models.TextField()
    guarantee = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    make_company = models.ForeignKey(MakeCompany, on_delete=models.DO_NOTHING)
    make_country = models.ForeignKey(MakeCountry, on_delete=models.DO_NOTHING)
    product_batch = models.ForeignKey(ProductBatch, on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to='products_img/', default='default_img/product_img.png')
    price = models.IntegerField()

    create_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name


class Review(models.Model):
    comment = models.CharField(max_length=200)
    star_given = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'review'

    def __str__(self):
        return f'{self.star_given} - {self.product.name} - {self.user.username if self.user else "Anonymous"}'

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return sum(item.product.price * item.quantity for item in self.cartitem_set.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)





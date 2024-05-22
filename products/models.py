from django.db import models
from django.shortcuts import render, redirect
from django.views import View
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


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


class Products(models.Model):
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




CustomUser = get_user_model()

class Review(models.Model):
    comment = models.CharField(max_length=200)
    star_given = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'review'

    def __str__(self):
        return f'{self.star_given} - {self.product.name} - {self.user.username if self.user else "Anonymous"}'








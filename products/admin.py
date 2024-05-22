from django.contrib import admin
from .models import Category, MakeCountry, MakeCompany, ProductBatch, Products, Review

admin.site.register(Category)
admin.site.register(MakeCompany)
admin.site.register(MakeCountry)
admin.site.register(ProductBatch)
admin.site.register(Products)
admin.site.register(Review)
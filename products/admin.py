from django.contrib import admin
from .models import Category, MakeCountry, MakeCompany, ProductBatch, Product, Review

admin.site.register(Category)
admin.site.register(MakeCompany)
admin.site.register(MakeCountry)
admin.site.register(ProductBatch)
admin.site.register(Product)
admin.site.register(Review)
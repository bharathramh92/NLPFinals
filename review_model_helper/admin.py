from django.contrib import admin
from review_model_helper.models import Product, ProductReviews
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')

admin.site.register(Product, ProductAdmin)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'review_text')

admin.site.register(ProductReviews, ProductReviewAdmin)
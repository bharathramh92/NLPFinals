from django.db import models


# Create your models here.
class Product(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=100, null= True, blank= True)
    description = models.CharField(max_length=500, null= True, blank= True)

    def __str__(self):
        return self.title


class ProductReviews(models.Model):
    product_id = models.ForeignKey(Product)
    review_text = models.CharField(max_length=1000, null=False, blank=False)

    def __str__(self):
        return self.review_text[:25]
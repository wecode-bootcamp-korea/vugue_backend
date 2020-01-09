from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'category'

class SubCategories(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'subcategory'

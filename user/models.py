from django.db import models

class User(models.Model):

    name       = models.CharField(max_length = 50, unique=True)
    password   = models.CharField(max_length = 500)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'users'

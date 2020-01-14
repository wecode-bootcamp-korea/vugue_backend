from django.db import models

class User(models.Model):

    name       = models.CharField(max_length = 200, unique=True, null=True)
    password   = models.CharField(max_length = 300, null = True)
    kakao      = models.CharField(max_length = 300, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'users'

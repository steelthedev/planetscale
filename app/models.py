from django.db import models



class Customers(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email

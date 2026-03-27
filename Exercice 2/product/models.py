from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=256)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    expiry_date = models.DateField()

    def __str__(self):
        return self.name

from django.db import models
import uuid


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=256, null=False)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=False)
    expiry_date = models.DateField(null=False)

    def __str__(self):
        return self.name

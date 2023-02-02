from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
class product(models.Model):
    productStatus = (("Active", "Active"), ("Inactive", "Inactive"))
    url = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    size = models.CharField(max_length=25, blank=True, null=True)
    price = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=20)
    created_time = models.DateTimeField(auto_now_add=True)
    phone_validation = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    status = models.CharField(max_length=30, choices=productStatus, default="Active")
    mobile_number = models.CharField(validators=[phone_validation], max_length=17, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class images(models.Model):
    product = models.ForeignKey(product, related_name="images", on_delete=models.CASCADE)
    image = models.TextField()

    def __str__(self):
        return self.product.title

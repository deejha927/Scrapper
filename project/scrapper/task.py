from celery import shared_task
from .models import *


@shared_task(bind=True)
def testingCelery(self):
    products = product.objects.filter(title__icontains="acer")
    print(products)
    return True


@shared_task(bind=True)
def workingTest(self):
    products = product.objects.filter(title__icontains="acer")
    print(products)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from celery.utils.log import get_task_logger
from django.shortcuts import render
from project.celery import app
from django.db import transaction
from bs4 import BeautifulSoup
from .models import *
from .task import *
import requests
import celery

# Create your views here.
def home(request):
    return render(request, "home.html")


# function check if data has text else return None
def textOrNone(element):
    value = None
    if element:
        value = element.text
    return value


# scarpes given url and return data in dict form
def scrapperData(url):
    headers = {
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Defined",
    }
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    category = soup.find_all("a", class_="_2whKao")
    title = soup.find("span", class_="B_NuCI")
    description = soup.find("div", class_="_1mXcCf RmoJUa")
    price = soup.find("div", class_="_30jeq3 _16Jk6d")
    size = soup.find("a", class_="_1fGeJ5 _2UVyXR _31hAvz")
    images = soup.find_all("img", class_="q6DClP")
    data = {
        "title": textOrNone(title),
        "description": textOrNone(description),
        "price": textOrNone(price),
        "size": textOrNone(size),
    }
    categories = []

    for val in category:
        categories.append(val.text)
    data["category"] = categories
    imageUrl = []
    for val in images:
        imageUrl.append(str(val["src"]).replace("128", "832"))
    data["imageUrl"] = imageUrl
    return data


@api_view(["POST"])
def scrapperUrlData(request):
    data = request.data
    try:
        scarper = scrapperData(data["url"])
        price = None
        if scarper["price"]:
            price = scarper["price"].split("₹")[1].replace(",", "")
        with transaction.atomic():
            createProduct = product.objects.create(
                description=scarper["description"],
                title=scarper["title"],
                size=scarper["size"],
                url=data["url"],
                price=price,
            )
            imagesList = []
            for val in scarper["imageUrl"]:
                productImage = images(product=createProduct, image=val)
                imagesList.append(productImage)
            if imagesList:
                images.objects.bulk_create(imagesList)
        return Response({"message": "Url Scrapped Succesfully", "state": True})
    except:
        return Response({"message": "Something went wrong", "state": False})


@api_view(["GET"])
def celeryWorker(request):
    testingCelery.delay()
    return Response("works")

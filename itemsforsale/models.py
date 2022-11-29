from django.db import models
from django.conf import settings
from django.urls import reverse
from django.forms import ModelForm

from accounts.models import CustomUser


class Item(models.Model):
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=20)
    image = models.ImageField(upload_to="images/", default="images/no-img.jpg")
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title + self.price

    def get_absolute_url(self):
        return reverse("item_detail", kwargs={"pk": self.pk})


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["title", "image", "price"]

    def get_absolute_url(self):
        return reverse("item_detail", kwargs={"pk": self.pk})

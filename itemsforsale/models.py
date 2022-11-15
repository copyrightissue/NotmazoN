from django.db import models
from django.conf import settings
from django.urls import reverse


class Item(models.Model):
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=20)
    image = models.ImageField(upload_to="images/%Y/%m/%d", blank=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("item_detail", kwargs={"pk": self.pk})


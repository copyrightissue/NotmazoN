from django.views.generic import ListView
from .models import Item


class ItemListView(ListView):
    model = Item
    template_name = 'item_list.html'

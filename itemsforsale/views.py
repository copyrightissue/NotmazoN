from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .models import Item


class ItemListView(ListView):
    model = Item
    template_name = 'item_list.html'


class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = "item_detail.html"


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = (
        "title",
        "image",
        "price",
        )
    template_name = "item_edit.html"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = "item_delete.html"
    success_url = reverse_lazy("item_list")

    def test_func(self): 
        obj = self.get_object()
        return obj.author == self.request.user


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = "item_new.html"
    fields = (
        "title",
        "image",
        "price",
    )

    def form_valid(self, form): 
        form.instance.author = self.request.user 
        return super().form_valid(form)

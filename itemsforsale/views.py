import logging
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .models import Item, ItemForm
from django.shortcuts import render, redirect


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
    template_name = "item_new.html"

    def get(self, request):
        logging.info('getting')
        return render(request, self.template_name, {'form': ItemForm()})

    def post(self, request):
        logging.info('posting')
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            # return redirect(request, "item_list.html")
            return redirect('item_list')


class SearchResultsView(ListView):
    model = Item
    context_object_name = "item_list"
    template_name = "search_results.html"

    def get_queryset(self): 
        query = self.request.GET.get("q")
        return Item.objects.filter( Q(title__icontains=query) | Q(price__icontains=query) )
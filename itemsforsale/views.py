import logging
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .models import Item, ItemForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages

class ItemListView(ListView):
    model = Item
    template_name = 'item_list.html'


class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = "item_detail.html"

    def get(self, request, pk): 
        logging.info('getting item detail view')
        return render(
            request, 
            self.template_name, 
            context={
                'item': self.get_object()
            },
        )
    
    def post(self, request, pk): 
        print('posting on item detail view')
        
        to_email = self.get_object().author.email
        print(f"sending email to: {to_email}")

        msg_html = render_to_string('email.html', {'logged_in_user': request.user, 'item': self.get_object()})

        send_mail(
            subject='Someone wants to purchase your item', 
            html_message=msg_html,
            message='Someone wants to purchase your item',
            from_email=None,
            recipient_list=[to_email], 
            fail_silently=False

        )
        messages.success(request, 'Your message has been sent to the seller.')
        return redirect('item_list')
        # return render(
        #     request,
        #     self.template_name,
        #     context={
        #         'item': self.get_object()
        #     },
        # )


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = (
        "title",
        "image",
        "description",
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
        return Item.objects.filter( Q(title__icontains=query))
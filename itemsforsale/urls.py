from django.urls import path
from .views import ItemListView, ItemDetailView, ItemDeleteView, ItemCreateView, ItemUpdateView, SearchResultsView

urlpatterns = [
    path("<int:pk>/", ItemDetailView.as_view(), name="item_detail"), 
    path("<int:pk>/edit/", ItemUpdateView.as_view(), name="item_edit"),
    path("<int:pk>/delete/", ItemDeleteView.as_view(), name="item_delete"),
    path("new/", ItemCreateView.as_view(), name="item_new"),
    path("search/", SearchResultsView.as_view(), name="search_results"),
    path('', ItemListView.as_view(), name="item_list"),
    ]

from django.conf import settings  # new
from django.conf.urls.static import static  # new
from django.urls import path
from .views import (
    BookListView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    book_detail_view,
    book_category_list,
    book_search_view,
)

app_name = 'books'

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('create/', BookCreateView.as_view(), name='book-create'),
    path('<int:id>/', book_detail_view, name='book-detail'),
    path('<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('books', book_category_list, name="book-by-category"),
    path('search/', book_search_view, name="search"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

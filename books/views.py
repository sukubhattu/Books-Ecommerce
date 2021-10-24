from django.db import models
from .models import Book, Review
from django.http import Http404
from django.shortcuts import redirect, render

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ReviewForm
from django.db.models import Q


class BookListView(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'books/book_list.html'
    ordering = ["-created"]
    paginate_by = 6


def book_category_list(request):
    try:
        category = request.GET['category']
    except:
        return redirect('books:book-list')
    page = request.GET.get('page', 1)
    books_ = Book.objects.filter(category__iexact=category)
    paginator = Paginator(books_, 2)

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    return render(request, 'books/book_list_category.html', {'books': books, 'category': category})


class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'books/book_detail.html'
    login_url = 'account_login'


@login_required
def book_detail_view(request, id):
    try:
        book = Book.objects.get(id=id)
        reviews = Review.objects.filter(book_id=id).order_by('-created')[:5]
    except Book.DoesNotExist:
        raise Http404('Book does not exist')
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = Review(review=form.cleaned_data['review'])
            review.book_id = id
            review.author_id = request.user.id
            review.save()
            return redirect('book-detail', book.id)
    else:
        form = ReviewForm()

    context = {'book': book, 'reviews': reviews, 'form': form}
    return render(request, 'books/book_detail.html', context)


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'books/book_create.html'
    fields = ['name', 'author', 'description', 'price', 'isbn', 'category', 'cover']

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(BookCreateView, self).get_form(form_class)
        form.fields['name'].widget.attrs = {'placeholder': 'Name of the book', 'class': ''}
        form.fields['author'].widget.attrs = {'placeholder': 'Name of author of book', 'class': ''}
        form.fields['description'].widget.attrs = {'placeholder': 'Short description about book', 'class': ''}
        form.fields['price'].widget.attrs = {'placeholder': 'Price of the book', 'step': 'any', 'class': ''}
        form.fields['isbn'].widget.attrs = {'placeholder': 'ISBN of the book', 'class': ''}
        form.fields['category'].widget.attrs = {'value': 'Select category of the book', 'class': ''}
        return form


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    template_name = 'books/book_update.html'
    fields = ['name', 'author', 'description', 'price', 'isbn', 'category', 'cover']

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

    def test_func(self):
        book = self.get_object()
        if self.request.user == book.seller:
            return True
        return False


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'books/book_delete.html'
    success_url = '/'

    def test_func(self):
        book = self.get_object()
        if self.request.user == book.seller:
            return True
        return False


def book_search_view(request):
    query = None
    if 'query' in request.GET and request.GET.get('query'):
        query = request.GET.get('query')
        books_ = Book.objects.filter(Q(name__icontains=query) | Q(isbn__icontains=query) | Q(author__icontains=query))
    if not query:
        return redirect('books:book-list')
    page = request.GET.get('page', 1)
    paginator = Paginator(books_, 2)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    return render(request, "books/search_result.html", {"books": books, "query": query})

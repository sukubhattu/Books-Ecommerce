from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from .models import UserPurchase, CustomUser
from books.models import Book
from .forms import PurchaseForm

# Create your views here.
@login_required
def user_profile(request):
    from users.models import CustomUser, UserPurchase
    from books.models import Book

    request_user_id = request.user.id
    user_data = {}
    if request_user_id:
        user = CustomUser.objects.get(id=request_user_id)
        listed_books = Book.objects.filter(seller_id=request_user_id)
        bought_books = UserPurchase.objects.filter(buyer_id=request_user_id)
        sold_books_not_paid = Book.objects.filter(seller_id=request_user_id, is_sold=True, is_paid=False)
        amount = 0
        for book in sold_books_not_paid:
            amount += book.price
        amount = amount * 0.95
        if request.method == 'POST':
            paypal_email = request.POST['paypalEmail']
            user.paypal_email_address = paypal_email
            user.save()
        # again querying user so that new email address is reflected on changing email
        user = CustomUser.objects.get(id=request_user_id)
        user_data = {'user': user, 'listed_books': listed_books, 'bought_books': bought_books, 'amount': amount}
        return render(request, 'account/profile.html', {'user_data': user_data})
    else:
        return redirect('books:book-list')


@login_required
def user_purchase_view(request, id):
    try:
        book = Book.objects.get(id=id)
        if book.seller_id == request.user.id:
            book = None
    except Book.DoesNotExist:
        raise Http404('Book does not exist')
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        if form.is_valid():
            user_purchase, new_user_purchase = UserPurchase.objects.get_or_create(
                seller=CustomUser.objects.get(id=book.seller_id),
                buyer=CustomUser.objects.get(id=request.user.id),
                book=Book.objects.get(id=id),
            )
            # user_purchase = UserPurchase(shipping_address=form.cleaned_data['shipping_address'])
            # user_purchase.seller = CustomUser.objects.get(id=book.seller_id)
            # user_purchase.buyer = CustomUser.objects.get(id=request.user.id)
            # user_purchase.book = Book.objects.get(id=id)
            # user_purchase.save()

            user_purchase.shipping_address = form.cleaned_data['shipping_address']
            user_purchase.save()

            return redirect('books:book-list')
    else:
        form = PurchaseForm()
    context = {'book': book, 'form': form}
    return render(request, 'books/book_purchase.html', context)

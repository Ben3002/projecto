from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db.models import Q


from .forms import ReviewForm
from .models import Item, Cart, CartItem, Review
from account.models import Account

# Create your views here.

def home_view(request):
        items = Item.objects.all()
        for item in items:
            item.average_rating = item.average_rating()  # Calculate average rating for each item
        return render(request, 'home.html', {'items': items})

def view_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    reviews = Review.objects.filter(item=item)

    context = {
        'item': item,
        'reviews' : reviews,
          }
    
    return render(request, 'core/view_item.html', context)

def view_items(request):
        context = {
            'items': Item.objects.all()
            }
        return render(request, "core/home.html", context)

def view_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()
        total_price = sum(item.price * item.quantity for item in items)
        return render(request, 'core/view_cart.html', {'items': items, 'total_price': total_price})
    else:
        return redirect('login')

def view_checkout(request):
    context = {}
    return render(request, 'core/checkout.html', context)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")



def add_to_cart(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(item=item, quantity=1)
    user_cart.items.add(cart_item)
    return redirect('view_cart')

def view_cart(request):
    if request.user.is_authenticated:
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = user_cart.items.all()
        total_price = sum(item.item.price * item.quantity for item in cart_items)
        return render(request, 'core/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})
    else:
        return redirect('login')

def remove_from_cart(request, item_id):
    item = Item.objects.get(pk=item_id)
    if request.user.is_authenticated:
        cart.items.remove(item)
        return redirect('core/view_cart')
    else:
        return redirect('login')

def add_review(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.user = request.user
            review.save()
            return redirect('view_item', item_id=item_id)
    else:
        form = ReviewForm()
    return render(request, 'core/add_review.html', {'form': form, 'item': item})


def all_reviews(request):
    reviews = Review.objects.all()
    print(reviews)
    return render(request, 'core/view_item.html', {'reviews': reviews})

def search(request):
    query = request.GET.get('q')
    results = Item.objects.filter(title__icontains=query)
    return render(request, 'core/search_results.html', {'results': results})
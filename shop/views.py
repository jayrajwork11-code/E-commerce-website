from decimal import Decimal

from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, Product


def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    selected_category = request.GET.get('category')

    if selected_category:
        products = products.filter(category__slug=selected_category)

    return render(request, 'shop/home.html', {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'shop/product_detail.html', {
        'product': product,
    })


def cart(request):
    cart_data = request.session.get('cart', {})
    items = []
    total = Decimal('0.00')

    if cart_data:
        products = Product.objects.filter(id__in=cart_data.keys())
        for product in products:
            quantity = cart_data.get(str(product.id), 0)
            subtotal = product.price * quantity
            total += subtotal
            items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })

    return render(request, 'shop/cart.html', {
        'items': items,
        'total': total,
    })


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    cart_data = request.session.get('cart', {})
    product_id = str(product.id)
    cart_data[product_id] = cart_data.get(product_id, 0) + 1
    request.session['cart'] = cart_data
    return redirect('shop:cart')


def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart_data = request.session.get('cart', {})
    product_id = str(product.id)

    if product_id in cart_data:
        del cart_data[product_id]
        request.session['cart'] = cart_data

    return redirect('shop:cart')

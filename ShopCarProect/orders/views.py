from cart.cart import Cart
from django.shortcuts import render 
from .forms import OrderCreateForm
from .models import OrderItem
import sqlite3
from django.core.mail import send_mail
from django.conf import settings

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            return render(request, 'orders/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html',
                  {'cart': cart, 'form': form})

def send_order(request):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM \"orders_orderitem\"")

    rows = cursor.fetchall()
    subject = 'Тема сообщения'
    message = ''
    for row in rows:
        message += f"Номер заказа: {row[0]}, Цена: {row[1]}, Количество: {row[2]},Номер товара: {row[4]}\n"
    conn.close()
    send_mail(subject, message, settings.EMAIL_HOST_USER, ['syperkek777@mail.ru'])
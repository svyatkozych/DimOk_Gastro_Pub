import json
import os
import requests
from django.shortcuts import render
from django.http import JsonResponse
from .models import Category, Dish, Order, OrderItem


def home_page(request):
    categories = Category.objects.all()
    dishes = Dish.objects.filter(is_available=True)
    return render(request, 'menu/index.html', {'categories': categories, 'dishes': dishes})


def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # 1. Зберігаємо замовлення в БД
            order = Order.objects.create(
                phone_number=data.get('phone'),
                delivery_type=data.get('delivery_type'),
                total_price=data.get('total'),
                delivery_cost=data.get('delivery_cost', 0),
                user_coords=json.dumps(data.get('coords'))
            )

            # 2. Зберігаємо товари
            items_list = ""
            for item in data['cart']:
                OrderItem.objects.create(
                    order=order,
                    dish_name=item['title'],
                    quantity=item['q'],
                    price=item['price']
                )
                items_list += f"• {item['title']} x{item['q']}\n"

            bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
            chat_id = os.getenv('TELEGRAM_CHAT_ID')

            geo_link = ""
            if data.get('coords'):
                geo_link = f"\n📍 <a href='https://www.google.com/maps?q={data['coords']['lat']},{data['coords']['lon']}'>Локація клієнта</a>"

            message = (
                f"🛍️ <b>НОВЕ ЗАМОВЛЕННЯ #{order.id}</b>\n"
                f"📞 Тел: {data['phone']}\n"
                f"🚚 Тип: {data.get('delivery_type')}\n"
                f"-------------------\n"
                f"{items_list}"
                f"-------------------\n"
                f"💵 Доставка: {data.get('delivery_cost')} ₴\n"
                f"💰 <b>РАЗОМ: {data.get('total')} ₴</b>"
                f"{geo_link}"
            )

            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",
                          data={'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'})

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
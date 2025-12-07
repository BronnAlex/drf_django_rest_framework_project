import stripe

from config.settings import STRIP_PAY_SECRET_KEY

stripe.api_key = STRIP_PAY_SECRET_KEY




def create_stripe_price(amount):
    """Принимает сумму на которую надо создать цену в stpipe """

    price = stripe.Price.create(
        currency="rub", # сумма будет в копейках, центах и тд, нашу сумму надо умножить на 100
        unit_amount=amount * 100,
        # recurring={"interval": "month"}, # регулярное списание раз  в месяц, нам не надо
        product_data={"name": "Оплата"},
    )
    return price


def create_stripe_session(price):
    """Создает сессию на оплату"""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")

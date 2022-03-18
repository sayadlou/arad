from ..store.models import Cart, CartItem


def cart_processor(request):
    context = {
        'cart': '',
        'cart_item': '',
        'cart_empty': True,
    }
    return context

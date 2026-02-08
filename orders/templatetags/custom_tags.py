from django import template

register = template.Library()

@register.filter
def multiply_price(quantity, food_name):
    """
    Multiply quantity by price stored in 'prices' dict in the context.
    """
    from django.template import Context
    # 'prices' must be available in the template context
    # We'll assume the context variable 'prices' exists
    try:
        # Access the 'prices' dictionary from the global context
        from django.template import base
        prices = base.Variable('prices').resolve(Context.current)
    except:
        prices = {}
    price = prices.get(food_name, 0)
    return quantity * price

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)

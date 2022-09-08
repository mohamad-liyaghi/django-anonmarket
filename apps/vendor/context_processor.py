def cart_items_counter(request):
    """Return Number of products in the cart"""

    if request.user.is_authenticated:
        return {"cart_count" : request.user.orders.count}

    return {"cart_count" : None}
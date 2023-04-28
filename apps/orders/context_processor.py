def order_counter(request):
    '''Return number of user orders'''

    if request.user.is_authenticated:
        return {"cart_count" : request.user.orders.filter(status__in=['o', 'a', 'p']).count()}

    return {"cart_count" : None}
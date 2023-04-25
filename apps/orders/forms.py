from django.forms import ModelForm
from orders.models import Order


class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = ("description",)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['placeholder']\
            = "Tell the vendor an address (not accurate)  \n if it was ok, vendor will send product to that address."

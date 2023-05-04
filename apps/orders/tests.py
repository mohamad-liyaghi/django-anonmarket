from django.test import TestCase
from accounts.models import Account
from products.models import Product
from orders.models import Order


class OrderTestCase(TestCase):
    def setUp(self) -> None:
        self.user = Account.objects.create(username='test username', password='1234EErr')
        self.product = Product.objects.create(title='title', provider=self.user)
        self.order = Order.objects.create(account=self.user, product=self.product)
        
    
    def test_order_token_generator(self):
        self.assertTrue(self.order.token)

    def test_order_provider_field(self):
            self.assertEqual(self.product.provider, self.order.provider)

    def test_order_price(self):
         self.assertEqual(self.product.price, self.order.price)
from django.test import TestCase
from accounts.models import Account
from products.models import Product, Category


class ProductTestCase(TestCase):
    def setUp(self) -> None:
        self.user = Account.objects.create(username='test username', password='1234EErr')
        self.product = Product.objects.create(title='title', provider=self.user)
        self.category = Category.objects.create(title='food')
    
    def test_slug_generator_for_product(self):
        self.assertTrue(self.product.slug)

    def test_slug_generator_for_category(self):
            self.assertTrue(self.product.slug)

    def test_category_name_lower(self):
         self.assertEqual(self.category.title, self.category.title.lower())
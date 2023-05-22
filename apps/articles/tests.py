from django.test import TestCase
from accounts.models import Account
from articles.models import Article, ArticlePurchase


class ArticleTestCase(TestCase):
    def setUp(self) -> None:
        self.user_a = Account.objects.create(username='test username', password='1234EErr', balance=10)
        self.user_b = Account.objects.create(username='test username2', password='1234EErr', balance=10)
        self.article = Article.objects.create(author=self.user_a, title='HI', price=10)

    def test_article_slug_generated(self):
            self.assertTrue(self.article.slug)

    def test_token_gen_for_article_purchase(self):
        purchase = ArticlePurchase.objects.create(user=self.user_b, article=self.article)
        self.assertTrue(purchase.token)

    def test_purchase_article(self):
        self.assertEqual(self.user_a.balance, 10)
        self.assertEqual(self.user_b.balance, 10)
        ArticlePurchase.objects.create(user=self.user_b, article=self.article)
        self.assertEqual(self.user_a.balance, 19)
        self.assertEqual(self.user_b.balance, 0)
         
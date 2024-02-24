from django.test import TestCase, Client
from rest_framework.test import APITestCase

from django.urls import reverse
from .views import *
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

"""class StockIntUrlTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Use the custom user model
        User = get_user_model()
        self.test_user = User.objects.create_user(username='testuser', password='testpassword')"""
        

class ArticleAndCategoryUrlTests(APITestCase):
    def setUp(self):
        self.client =  APIClient()
        # Use the custom user model
        User = get_user_model()
        self.test_user = User.objects.create_user(username='minor', password='minor')

    def test_statistique_stock_int_month_url(self):
        # Force authenticate the test user for this request
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(reverse('statistique_stock_int_month', args=[2023]))
        self.assertEqual(response.status_code,  200)
       

    def test_statistique_stock_int_year_url(self):
        # Force authenticate the test user for this request
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(reverse('statistique_stock_int_year'))
        self.assertEqual(response.status_code,  200)
        

    def test_statistique_stock_int_day_url(self):
        # Force authenticate the test user for this request
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(reverse('statistique_stock_int_day', args=[2023,  12]))
        self.assertEqual(response.status_code,  200)

    def test_statistique_stock_int_month_article_url(self):
        # Force authenticate the test user for this request
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(reverse('statistique_stock_int_month_article', args=[2023, 'example_article']))
        self.assertEqual(response.status_code,  200)
        

    def test_statistique_stock_int_year_article_url(self):
        # Force authenticate the test user for this request
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(reverse('statistique_stock_int_year_article', args=['example_article']))
        self.assertEqual(response.status_code,  200)
        
    def test_statistique_stock_int_day_article_url(self):
        # Force authenticate the test user for this request
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(reverse('statistique_stock_int_day_article', args=[2023,  12, 'example_article']))
        self.assertEqual(response.status_code,  200)
    def test_statistique_stock_category_int_month_url(self):
        # Force authenticate the test user for this request
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(reverse('statistique_stock_category_int_month', args=[2023]))
        self.assertEqual(response.status_code,  200)
        

    def test_statistique_stock_category_int_year_url(self):
        # Force authenticate the test user for this request
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(reverse('statistique_stock_category_int_year'))
        self.assertEqual(response.status_code,  200)
        

    def test_statistique_stock_category_int_day_url(self):
        # Force authenticate the test user for this request
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(reverse('statistique_stock_category_int_day', args=[2023,  12]))
        self.assertEqual(response.status_code,  200)
        
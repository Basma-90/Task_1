from typing import Any
from django.test import TestCase
# taskApi/tests.py
from django.test import TestCase
from .models import Task

class ProductTestCase(TestCase):
    def setUp(self):
        Task.objects.create(name="Test Product", description="Test Description", location="Test Location", price=99.99, color="Test Color")

    def test_product_attributes(self):
        test_product = Task.objects.get(name="Test Product")
        self.assertEqual(test_product.description, "Test Description")






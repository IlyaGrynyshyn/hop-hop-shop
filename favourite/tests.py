# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from shop.models import Product
# from django.test import TestCase
# from django.contrib.sessions.middleware import SessionMiddleware
# from django.test.client import RequestFactory
# from .services import FavouriteService
#
#
# class FavouriteViewsTests(APITestCase):
#     def setUp(self):
#         self.product = Product.objects.create(
#             name="Test Product",
#             category="Test Category",
#             slug="test-product",
#             price=10.00,
#             SKU="12345",
#             description="Test Description",
#             views=0,
#         )
#         self.add_url = reverse("add_to_favourites", args=[self.product.id])
#         self.remove_url = reverse("remove_from_favourites", args=[self.product.id])
#         self.view_url = reverse("view_favourites")
#         self.clear_url = reverse("clear_favourites")
#
#     def test_add_to_favourites(self):
#         response = self.client.post(self.add_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("product", response.data)
#         self.assertEqual(response.data["product"]["id"], self.product.id)
#
#     def test_remove_from_favourites(self):
#         self.client.post(self.add_url)
#         response = self.client.post(self.remove_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_view_favourites(self):
#         self.client.post(self.add_url)
#         response = self.client.get(self.view_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data["products"]), 1)
#
#     def test_clear_favourites(self):
#         self.client.post(self.add_url)
#         response = self.client.post(self.clear_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         response = self.client.get(self.view_url)
#         self.assertEqual(len(response.data["products"]), 0)
#
#
# class FavouriteServiceTests(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.request = self.factory.get("/")
#         middleware = SessionMiddleware()
#         middleware.process_request(self.request)
#         self.request.session.save()
#
#         self.product = Product.objects.create(
#             name="Test Product",
#             category="Test Category",
#             slug="test-product",
#             price=10.00,
#             SKU="12345",
#             description="Test Description",
#             views=0,
#         )
#
#     def test_add_product(self):
#         service = FavouriteService(self.request.session)
#         service.add_product(self.product.id)
#         self.assertIn(self.product.id, service.favourites)
#
#     def test_remove_product(self):
#         service = FavouriteService(self.request.session)
#         service.add_product(self.product.id)
#         service.remove_product(self.product.id)
#         self.assertNotIn(self.product.id, service.favourites)
#
#     def test_clear(self):
#         service = FavouriteService(self.request.session)
#         service.add_product(self.product.id)
#         service.clear()
#         self.assertEqual(service.favourites, [])
#
#     def test_get_products(self):
#         service = FavouriteService(self.request.session)
#         service.add_product(self.product.id)
#         products = service

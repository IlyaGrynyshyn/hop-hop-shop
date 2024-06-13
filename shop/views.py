from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from shop.models import Category, Product, ProductImage
from shop.serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductDetailSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from shop.filters import ProductFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="category",
                description="Specify the category slug to filter the products.",
                required=False,
                type=str,
            ),
        ]
    )
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def popular(self, request):
        """
        Retrieve the top 30 most viewed products.

        Returns:
            Response: Serialized data of the top 30 most viewed products.
        """
        popular_products = Product.objects.order_by("-views")[:30]
        serializer = self.get_serializer(popular_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="upload-images")
    def upload_images(self, request, pk=None):
        product = self.get_object()
        uploaded_images = request.FILES.getlist("uploaded_images")

        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

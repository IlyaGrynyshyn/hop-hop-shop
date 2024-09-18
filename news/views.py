from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from news.filters import NewsFilter
from utils.pagination import Pagination

from news.models import News
from news.serializers import NewsListSerializer, NewsDetailSerializer


@extend_schema(tags=["news"])
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    filterset_class = NewsFilter
    pagination_class = Pagination
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_serializer_class(self):
        if self.action == 'list':
            return NewsListSerializer
        else:
            return NewsDetailSerializer

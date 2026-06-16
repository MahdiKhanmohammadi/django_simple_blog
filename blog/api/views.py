from rest_framework.viewsets import ModelViewSet
from .serializer import CategoryModelSerializer, PostListModelSerializer, PostWriteModelSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from blog.models import Category, Post
from .pagination import DefaultPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class CategoryModelViewSet(ModelViewSet):
    serializer_class = CategoryModelSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title']
    ordering_fields = ['created_date', 'updated_date']


class PostModelViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostWriteModelSerializer
        else:
            return PostListModelSerializer

    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'category', 'author']
    search_fields = ['title', 'category']
    ordering_fields = ['created_date', 'updated_date']

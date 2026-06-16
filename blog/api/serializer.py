from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import PrimaryKeyRelatedField, HyperlinkedRelatedField
from blog.models import Category, Post


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ['created_date', 'updated_date']


class PostWriteModelSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ['created_date', 'updated_date']


class PostListModelSerializer(ModelSerializer):
    category = CategoryModelSerializer()

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ['created_date', 'updated_date']

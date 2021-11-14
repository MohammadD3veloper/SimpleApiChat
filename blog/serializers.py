from rest_framework.serializers import Serializer
from .models import News


class BlogSerializer(Serializer):
    class Meta:
        model = News
        fields = [
            'title',
            'slug',
            'image',
            'text',
            'date',
            'author',
            'published',
        ]
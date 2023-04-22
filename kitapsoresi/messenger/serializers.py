import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from messenger.models import Books

# class BookModel:
#     def __init__(self, name, description):
#         self.name = name
#         self.description = description

class BooksSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Books
        fields = "__all__"
        # fields = ("name", "slug", "author", "description", "genre", "price", "is_published")
    # name = serializers.CharField(max_length=255)
    # slug = serializers.SlugField(max_length=255)
    # author = serializers.CharField(max_length=255)
    # # photo = serializers.ImageField()
    # description = serializers.CharField()
    # # genre = serializers.CharField(default="не выбрано")
    # price = serializers.IntegerField()
    # is_published = serializers.BooleanField(default=True)
    # # time_create = serializers.DateTimeField(read_only=True)
    # # time_update = serializers.DateTimeField(read_only=True)
    #
    # def create(self, validated_data):
    #     return Books.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.slug = validated_data.get("slug", instance.slug)
    #     instance.author = validated_data.get("author", instance.author)
    #     instance.description = validated_data.get("description", instance.description)
    #     instance.price = validated_data.get("price", instance.price)
    #     instance.is_published = validated_data.get("is_published", instance.is_published)
    #     # instance.time_update = validated_data.get("time_update", instance.time_update)
    #     instance.save()
    #     return instance



# def encode():
#     model = BookModel('name', 'ggdkmbkdmb')
#     model_sr = BooksSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
# def decode():
#     stream = io.BytesIO(b'{"name":"name", "description":"fhuihegnieg"}')
#     data = JSONParser().parse(stream)
#     serializer = BooksSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)
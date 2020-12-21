from rest_framework import serializers

from shop.models import Product, Attribute, Value


class ValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Value
        fields = ['value']


class AttributeSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = Attribute
        fields = ['name', 'value']

    def get_value(self, instance):
        return instance.value.value


class ProductSerializer(serializers.ModelSerializer):
    attribute = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    subcategory = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'sku', 'description', 'created_at', 'price',
                  'subcategory', 'category', 'attribute']
        depth = 1

    def get_attribute(self, intsance):
        serializer = AttributeSerializer(intsance.attribute.all(), many=True)
        return serializer.data

    def get_category(self, instance):
        return instance.subcategory.category.name

    def get_subcategory(self, instance):
        return instance.subcategory.name

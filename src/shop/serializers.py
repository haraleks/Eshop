from rest_framework import serializers

from shop.models import Product, Value, Category, Subcategory, Feedback, ProductsCompare, DesiredProducts, \
    PositionProduct, Basket
from users.constants import Status


class ValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Value
        fields = ['value']


class AttributeSerializer(serializers.ModelSerializer):
    attribute = serializers.SerializerMethodField()

    class Meta:
        model = Value
        fields = ['attribute', 'value']

    def get_attribute(self, instance):
        return instance.attribute.name


class ProductSerializer(serializers.ModelSerializer):
    characteristic = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    subcategory = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'sex', 'sku', 'description', 'created_at', 'price',
                  'category', 'subcategory', 'characteristic']
        depth = 1

    def get_characteristic(self, intsance):
        serializer = AttributeSerializer(intsance.value_model.all(), many=True)
        return serializer.data

    def get_category(self, instance):
        if instance.subcategory:
            return instance.subcategory.category.name
        return ''

    def get_subcategory(self, instance):
        if instance.subcategory:
            return instance.subcategory.name
        return ''


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = '__all__'


class ProductDetailSerializer(ProductSerializer):
    feedback = FeedbackSerializer(Feedback.objects.all(), many=True)
    same_product = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'sex', 'description', 'created_at', 'price',
                  'category', 'subcategory', 'characteristic', 'feedback', 'same_product']

    def get_same_product(self, instance):
        customer = self.context['request'].user.client_profile
        product_random = Product.objects.random(sex=customer.sex,
                                                subcategory=instance.subcategory,
                                                exclud_id=instance.pk,
                                                age=customer.age)
        serializers = ProductSerializer(product_random[:5], many=True)
        return serializers.data


class SubcategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Subcategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    subcategory = SubcategorySerializer(Subcategory.objects.all(), many=True)

    class Meta:
        model = Category
        fields = '__all__'


class ProductsCompareSerializer(serializers.ModelSerializer):
    # products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = ProductsCompare
        fields = ['id', 'products']

    def create(self, validated_data):
        customer = self.context['request'].user.client_profile
        product_compare = ProductsCompare.objects.create(**validated_data)
        product_compare.customer = customer
        product_compare.save()
        product_compare.refresh_from_db()
        return product_compare

    def validate(self, attrs):
        customer = self.context['request'].user.client_profile
        count_record = ProductsCompare.objects.filter(customer=customer).count()
        if count_record >= 5:
            raise serializers.ValidationError({"Records": ["Maximum of 5 entries"]})
        return attrs


class WishListSerializer(serializers.ModelSerializer):

    class Meta:
        model = DesiredProducts
        fields = ['id', 'product']

    def create(self, validated_data):
        customer = self.context['request'].user.client_profile
        product = validated_data.pop('product')
        wish_list = DesiredProducts.objects.create(customer=customer,
                                                   product=product)
        return wish_list

    def validate(self, attrs):
        customer = self.context['request'].user.client_profile
        is_product = DesiredProducts.objects.filter(customer=customer, product=attrs['product']).exists()
        if is_product:
            raise serializers.ValidationError({'Product:': "You added this product in your wish list"})
        return super().validate(attrs)


class SubWishListSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Subcategory
        fields = ['name', 'products']

    def get_products(self, instance):
        products = instance.product.filter(id__in=[p.product.id for p in self.context['queryset']])
        return ProductSerializer(products, many=True).data


class AddedProductInBasketSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField()

    def create(self, validated_data):
        customer = self.context['request'].user.client_profile
        basket = Basket.objects.filter(customer=customer,
                                       status=Status.CREATED.value).order_by('pk').last()
        if not basket:
            basket = Basket.objects.create(status=Status.CREATED.value,
                                           customer=customer)
        product = Product.objects.get(pk=validated_data.pop('product'))
        position_product = PositionProduct.objects.create(product_items=product.product_items,
                                                          quantity=validated_data['quantity'],
                                                          basket=basket)
        return position_product

    def validate(self, attrs):
        if attrs['product'].product_items.remains == 0:
            raise serializers.ValidationError({"Product": "Product is over"})
        return super().validate(attrs)


class PositionProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = PositionProduct
        fields = ['id', 'product_name', 'product_price', 'quantity', 'total_product_price']


class BasketSerializer(serializers.ModelSerializer):
    position_products = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ['id', 'position_products', 'customer', 'create_at',
                  'promocode', 'status', 'total_order', 'discount',
                  'total_with_discount']

    def get_position_products(self, instance):
        position_products = instance.position_product.all()
        return PositionProductSerializer(position_products, many=True).data


class SendPayBasketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Basket
        fields = ['id', 'status']
        read_only_fields = ['customer', 'create_at', 'promocode']

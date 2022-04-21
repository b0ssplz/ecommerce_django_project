from rest_framework import serializers
from decimal import Decimal
from store.models import Product, Collection, Review


# class CollectionSeralizer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField()
    
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','date', 'name', 'description', 'product']    
    
class CollectionSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title']
    
# class ProductSeralizer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     price_taxxed = serializers.SerializerMethodField(method_name='calculate_tax')
#     #collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())
#     #collection = serializers.StringRelatedField()
#     #collection = CollectionSeralizer()
#     #title = serializers.HyperlinkedRelatedField(queryset=Product.objects.all, view_name='product-detail')
#     collection = serializers.HyperlinkedRelatedField(queryset=Collection.objects.all, view_name='collection-detail')
    
#     def calculate_tax(self, product:Product):
#         return product.price * Decimal(1.23)
    
    
class ProductSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','description','slug', 'inventory','price','price_taxxed','collection']
    
    #title =  serializers.HyperlinkedRelatedField(queryset=Product.objects.all, view_name='product-detail')
    #collection = serializers.HyperlinkedRelatedField(queryset=Collection.objects.all, view_name='collection-detail')
    price_taxxed = serializers.SerializerMethodField(method_name='calculate_tax')
    collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())
        
    def calculate_tax(self, product:Product):
        return product.price * Decimal(1.23)
    
    # def validate(self,data):
    #     if data[''] != data['']:
    #         return serializers.ValidationError('error')
    
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
        
    #     return product

    # def update(self, instance, validated_data):
    #     instance.price = validated_data.get('price')
    #     instance.save()
        
    #     return instance
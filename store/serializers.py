from rest_framework import serializers
from decimal import Decimal
from store.models import Product, Collection, Review, Cart, CartItem


# class CollectionSeralizer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField()
    
    

        
        

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','date', 'name', 'description']   
        
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data) 
    
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
    
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','price']
        
        
class CartItemSerializer(serializers.ModelSerializer):
    
    #product = ProductSeralizer()
    product = SimpleProductSerializer()
    class Meta:
        model = CartItem
        fields = ['id','product','quantity', 'total_price']
        
    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')
        
    def calculate_total_price(self, cart_item:CartItem):
        return cart_item.quantity * cart_item.product.price
    
class CartSerializer(serializers.ModelSerializer):
    
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_cart_price = serializers.SerializerMethodField(method_name='calculate_total_cart_price')
 
    def calculate_total_cart_price(self, cart:Cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])
    
    class Meta:
        model = Cart
        fields = ['id','items', 'total_cart_price']
    
class AddCartItemSerializer(serializers.ModelSerializer):
    
    product_id = serializers.IntegerField()
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        
        try: #update old item (quantity)
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity +=quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist: #add new item
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
            
        return self.instance
    
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']
        
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
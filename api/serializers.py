from rest_framework import serializers
from .models import Product , Review , Order , OrderItem , ShippingAdress
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ProductSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    reviews = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
    
    def get_reviews(self,obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews,many=True)
        return serializer.data    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user','product','comment','created']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class ShippingAdressSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ShippingAdress
        fields = '__all__'        

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    orderitems = serializers.SerializerMethodField(read_only=True)
    shippingadress = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

    def get_user(self,obj):
        user = obj.user
        serializer = UserSerializer(user,many=False)
        return serializer.data     
    
    def get_orderitems(self,obj):
        orderitems = obj.orderitem_set.all()
        serializer = OrderItemSerializer(orderitems,many=True)
        return serializer.data
    
    def get_shippingadress(self,obj):
        shippingadress = obj.shippingadress_set.all()
        serializer = ShippingAdressSerializer(shippingadress,many=True)
        return serializer.data
        
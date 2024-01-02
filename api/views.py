from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product , Order , OrderItem , ShippingAdress
from . serializers import ProductSerializer , OrderSerializer
# Create your views here.

@api_view(['GET','POST'])
def productsList(request):
    if request.method == 'GET':
        query = request.GET.get('query') or ''
        products = Product.objects.filter(name__icontains=query)
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        new_product = Product.objects.create(
            user = request.user,
            name = request.data['name'],
            image = request.data['image'],
            description = request.data['description'],
            brand = request.data['brand'],
            category = request.data['category'],
            rating = request.data['rating'],
            countInstock = request.data['countInstock']
        )
        new_product.save()

        serializer = ProductSerializer(new_product,many=False)
        return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])    
def productsDetails(request,pk):
    product = Product.objects.get(_id=pk)
    if request.method == 'GET':
        serializer = ProductSerializer(product,many=False)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        product.name = request.data['name']
        product.description = request.data['description']
        product.brand = request.data['brand']
        product.category = request.data['category']
        product.rating = request.data['rating']
        product.countInstock = request.data['countInstock']
        
        product.save()
        serializer = ProductSerializer(product,many=False)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        product.delete()
        return Response('Product deleted successfully!')
    
@api_view(['GET'])
def topProducts(request):
    if request.method == 'GET':
        products = Product.objects.filter(rating__gte=4)
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)    
    
@api_view(['GET'])
def allOrders(request):
    order = Order.objects.all()
    serializer = OrderSerializer(order,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def myOrder(request):
    order = request.user.order_set.all()
    serializer = OrderSerializer(order,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def OrderById(request,pk):
    try:
        order = Order.objects.get(_id=pk)
        if request.user.is_staff or order.user == request.user:
            serializer = OrderSerializer(order,many=False)
            return Response(serializer.data)
        else:
            return Response({'detail':'Not authorized to view this order.'},status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'error':'Order does not exist'},status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def addOrderItems(request):
    orderItems = request.data['orderitems']
    
    if len(orderItems) == 0 :
        return Response({'detail':'No order Items'},status=status.HTTP_400_BAD_REQUEST)
    else:
        order = Order.objects.create(
        user = request.user,
        payment_method = request.data['payment_method'],
        taxPrice = request.data['taxPrice'],
        shippingPrice = request.data['shippingPrice'],
        totalPrice = request.data['totalPrice'],
        )    
    
    Shippingadress = ShippingAdress.objects.create(
        order = order,
        adress = request.data['shippingadress']['adress'],
        city = request.data['shippingadress']['city'],
        zipcode = request.data['shippingadress']['zipcode'],
        country = request.data['shippingadress']['country']
        )

    for i in orderItems:
        product = Product.objects.get(_id=i['product'])
        item = OrderItem.objects.create(
            product = product,
            order = order,
            name = product.name,
            quantity = i['quantity'],
            price = i['price']
            )
        product.countInstock -= item.quantity

        product.save()
    
    serializer = OrderSerializer(order,many=False)   
    return Response(serializer.data)

        





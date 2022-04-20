from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Collection
from .serializers import CollectionSeralizer, ProductSeralizer
from rest_framework import status

# Create your views here.

@api_view(['GET', 'POST'])
def product_list(request):
    
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        #queryset = Product.objects.all() lazy loading
        serializer = ProductSeralizer(queryset, many=True, context={'request':request})
        return Response(serializer.data)
    
    # elif request.method == 'POST':
    #     serializer = ProductSeralizer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.validated_data
    #         return Response("ok")
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        serializer = ProductSeralizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #serializer.validated_data
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)



# @api_view()
# def product_detail(request, id):
#     try:
#         product = Product.objects.get(pk=id)
#         serializer = ProductSeralizer(product)
#         return Response(serializer.data)
#     except Product.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET','PUT','DELETE'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'GET':
        serializer = ProductSeralizer(product, context={'request':request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProductSeralizer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        if product.orderitem_set.count() > 0:
            return Response({'error': "cant delete"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def collection_list(request):
    
    if request.method == 'GET':
        queryset = Collection.objects.all()
        serializer = CollectionSeralizer(queryset, many=True, context={'request':request})
        return Response(serializer.data)
    
    
    elif request.method == 'POST':
        serializer = CollectionSeralizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #serializer.validated_data
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)




@api_view(['GET','PUT','DELETE'])
def collection_detail(request, pk):
    
    collection = get_object_or_404(Collection, pk=pk)

    if request.method == 'GET':
        serializer = CollectionSeralizer(collection, context={'request':request})
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = CollectionSeralizer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    if request.method == 'DELETE':
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
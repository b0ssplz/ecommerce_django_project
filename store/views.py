from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Collection, OrderItem, Review
from .serializers import CollectionSeralizer, ProductSeralizer, ReviewSerializer
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet    

from store import serializers


# ------------- Viewsets -------------------



class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer






class CollectionViewSet(ModelViewSet):
    
    queryset = Collection.objects.all()
    serializer_class = CollectionSeralizer
    
    def get_serializer_context(self):
        return {'request': self.request}  
    
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']):
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)    

    # def delete(self,request, pk): #overriding
    #     collection = get_object_or_404(Collection, pk=pk)
    #     if collection.orderitem_set.count() > 0:
    #         return Response({'error': "cant delete"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    #     collection.delete()
        
    #     return Response(status=status.HTTP_204_NO_CONTENT) 

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSeralizer 

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'whoa hol up'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)

# ------------- Class Views -------------------


class CollectionList(ListCreateAPIView):
    
    queryset = Collection.objects.all()
    serializer_class = CollectionSeralizer
    
    def get_serializer_context(self):
        return {'request': self.request}


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    
    queryset = Collection.objects.all()
    serializer_class = CollectionSeralizer

    def delete(self,request, pk): #overriding
        collection = get_object_or_404(Collection, pk=pk)
        if collection.orderitem_set.count() > 0:
            return Response({'error': "cant delete"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        collection.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT) 



class ProductList(ListCreateAPIView):
    
    queryset = Product.objects.all()
    serializer_class = ProductSeralizer
    
    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()
    
    # def get_serializer_class(self):
    #     return ProductSeralizer
    
    def get_serializer_context(self):
        return {'request': self.request}
    

# class ProductList(APIView):
    
#     def get(self,request):
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSeralizer(queryset, many=True, context={'request':request})
#         return Response(serializer.data)
    
#     def post(self,request):
#         serializer = ProductSeralizer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
        
#         return Response(serializer.data, status=status.HTTP_201_CREATED)       
        

class ProductDetail(RetrieveUpdateDestroyAPIView):
    
    queryset = Product.objects.all()
    serializer_class = ProductSeralizer

    def delete(self,request, pk): #overriding
        product = get_object_or_404(Product, pk=pk)
        if product.orderitem_set.count() > 0:
            return Response({'error': "cant delete"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        product.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT) 


# class ProductDetail(APIView):
    
#     def get(self,request, pk):
#         product = get_object_or_404(Product, pk=pk)
        
#         serializer = ProductSeralizer(product, context={'request':request})
#         return Response(serializer.data)    

    
#     def put(self,request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         serializer = ProductSeralizer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
        
#         return Response(serializer.data)


#     def delete(self,request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitem_set.count() > 0:
#             return Response({'error': "cant delete"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
#         product.delete()
        
#         return Response(status=status.HTTP_204_NO_CONTENT) 



# ------------- Function Views -------------------


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
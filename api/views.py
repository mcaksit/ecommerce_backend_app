from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomerSerializer
from .models import Customer

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List':'/customer-list/',
        'Detail':'/customer-detail/<str:pk>/',
        'Create':'/customer-create/',
        'Update':'/customer-update/<str:pk>/',
        'Delete':'/customer-delete/<str:pk>/',
    }
    return Response(api_urls)

@api_view(['GET'])
def CustomerList(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def CustomerDetail(request, pk):
    customers = Customer.objects.get(id=pk)
    serializer = CustomerSerializer(customers, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def CustomerCreate(request):
    serializer = CustomerSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST'])
def CustomerUpdate(request, pk):
    customer = Customer.objects.get(id=pk)
    serializer = CustomerSerializer(instance=customer, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def CustomerDelete(request, pk):
    customer = Customer.objects.get(id=pk)
    customer.delete()

    return Response('Customer Deleted Successfully!')
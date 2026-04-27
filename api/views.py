from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Category, MenuItem, Reservation, Order, OrderItem
from .serializers import (
    CategorySerializer, MenuItemSerializer, ReservationSerializer, 
    OrderOutputSerializer, OrderItemInputSerializer, UserRegistrationSerializer
)
from .management.commands.seed_menu import Command as SeedMenuCommand

class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

class MyTokenObtainPairView(TokenObtainPairView):
    pass

class MenuListView(APIView):
    def get(self, request):
        category_slug = request.query_params.get('category', 'all')
        menu_items = MenuItem.objects.select_related('category').filter(is_available=True)
        if category_slug != 'all':
            menu_items = menu_items.filter(category__slug=category_slug)
        return Response(MenuItemSerializer(menu_items, many=True).data)

class MenuDetailView(APIView):
    def get(self, request, pk):
        menu_item = get_object_or_404(MenuItem, pk=pk, is_available=True)
        return Response(MenuItemSerializer(menu_item).data)

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.prefetch_related('items').all()
        return Response(CategorySerializer(categories, many=True).data)

class ReservationListCreateView(APIView):
    def get(self, request):
        reservations = Reservation.objects.all()
        return Response(ReservationSerializer(reservations, many=True).data)

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            reservation = serializer.save()
            return Response(ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservationDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Reservation, pk=pk)

    def get(self, request, pk):
        reservation = self.get_object(pk)
        return Response(ReservationSerializer(reservation).data)

    def patch(self, request, pk):
        reservation = self.get_object(pk)
        serializer = ReservationSerializer(reservation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reservation = self.get_object(pk)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderListCreateView(APIView):
    def get(self, request):
        orders = Order.objects.prefetch_related('items__menu_item').all()
        return Response(OrderOutputSerializer(orders, many=True).data)

    @transaction.atomic
    def post(self, request):
        items_data = request.data.get('items', [])
        note = request.data.get('note', '')
        if not items_data:
            return Response({'error': 'Кошик порожній'}, status=status.HTTP_400_BAD_REQUEST)
        input_ser = OrderItemInputSerializer(data=items_data, many=True)
        if not input_ser.is_valid():
            return Response(input_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        ids = [i['id'] for i in input_ser.validated_data]
        menu_items = {m.id: m for m in MenuItem.objects.filter(id__in=ids, is_available=True)}
        missing = set(ids) - set(menu_items.keys())
        if missing:
            return Response({'error': f'Позиції не знайдено: {list(missing)}'}, status=status.HTTP_400_BAD_REQUEST)
        total = sum(menu_items[i['id']].price * i['qty'] for i in input_ser.validated_data)
        order = Order.objects.create(total_price=total, note=note)
        for item_data in input_ser.validated_data:
            mi = menu_items[item_data['id']]
            OrderItem.objects.create(
                order=order,
                menu_item=mi,
                quantity=item_data['qty'],
                unit_price=mi.price,
            )
        return Response(OrderOutputSerializer(order).data, status=status.HTTP_201_CREATED)

class OrderDetailView(APIView):
    def get(self, request, pk):
        order = get_object_or_404(Order.objects.prefetch_related('items__menu_item'), pk=pk)
        return Response(OrderOutputSerializer(order).data)

class OrderStatusUpdateView(APIView):
    ALLOWED_TRANSITIONS = {
        'new': ['preparing', 'cancelled'],
        'preparing': ['ready', 'cancelled'],
        'ready': ['completed'],
        'completed': [],
        'cancelled': [],
    }

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        new_status = request.data.get('status')
        if not new_status:
            return Response({'error': 'Поле status обов\'язкове'}, status=status.HTTP_400_BAD_REQUEST)
        allowed = self.ALLOWED_TRANSITIONS.get(order.status, [])
        if new_status not in allowed:
            return Response(
                {'error': f'Перехід з «{order.status}» → «{new_status}» неможливий. Дозволено: {allowed}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order.status = new_status
        order.save(update_fields=['status'])
        return Response(OrderOutputSerializer(order).data)

class SeedMenuView(APIView):
    def get(self, request):
        command = SeedMenuCommand()
        command.handle(clear=True)
        return Response({"message": "Menu seeded successfully!"}, status=status.HTTP_200_OK)
from rest_framework import filters as rf_filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import RoomSerializer, BookingSerializer, CarouselSerializer, MyBookingSerializer
from .models.room import Room
from .models.booking import Booking
from .models.carousel import Carousel


class RoomResultSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'


class MyBookingResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class ProductFilter(filters.FilterSet):
    min_capacity = filters.NumberFilter(field_name="capacity", lookup_expr='gte')
    equipment = filters.AllValuesFilter(field_name="equipment__name")

    class Meta:
        model = Room
        fields = ['min_capacity', 'equipment']


class RoomViewSet(ReadOnlyModelViewSet):
    filter_backends = [rf_filters.SearchFilter, DjangoFilterBackend]
    pagination_class = RoomResultSetPagination
    serializer_class = RoomSerializer
    search_fields = ['address', ]
    filterset_class = ProductFilter
    queryset = Room.objects.get_queryset().order_by('id')


class CarouselViewSet(ReadOnlyModelViewSet):
    serializer_class = CarouselSerializer
    queryset = Carousel.objects.all()


class BookingViewSet(ModelViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated, ]


class MyBookingViewSet(ReadOnlyModelViewSet):
    pagination_class = MyBookingResultSetPagination
    serializer_class = MyBookingSerializer
    queryset = Booking.objects.get_queryset().order_by('id')
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        total = Booking.objects.filter(user=self.request.user).count()
        if total > 50:
            queryset = Booking.objects.filter(user=self.request.user)[total - 50:total]
            return queryset

        queryset = Booking.objects.filter(user=self.request.user)
        return queryset

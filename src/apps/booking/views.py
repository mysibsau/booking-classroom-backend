from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import RoomSerializer, BookingSerializer, CarouselSerializer, MyBookingSerializer
from .models.room import Room
from .models.booking import Booking
from .models.carousel import Carousel


class ResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'


class RoomViewSet(ReadOnlyModelViewSet):
    pagination_class = ResultsSetPagination
    serializer_class = RoomSerializer
    filter_fields = ['address', 'capacity', ]
    queryset = Room.objects.get_queryset().order_by('id')


class CarouselViewSet(ReadOnlyModelViewSet):
    serializer_class = CarouselSerializer
    queryset = Carousel.objects.all()


class BookingViewSet(ModelViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated, ]


class MyBookingViewSet(ReadOnlyModelViewSet):
    serializer_class = MyBookingSerializer
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

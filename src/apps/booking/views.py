import django_filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import RoomSerializer, BookingSerializer
from .models.room import Room
from .models.booking import Booking


class ResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'


class RoomViewSet(ReadOnlyModelViewSet):
    pagination_class = ResultsSetPagination
    serializer_class = RoomSerializer
    filter_fields = ['address', 'capacity', ]
    queryset = Room.objects.get_queryset().order_by('id')


class BookingViewSet(ModelViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        if self.action == "my":
            return self.queryset.filter(user=self.request.user)
        return self.queryset

    @action(detail=False)
    def my(self, request):
        return super().list(request)


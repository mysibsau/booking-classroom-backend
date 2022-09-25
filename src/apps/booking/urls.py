from rest_framework.routers import SimpleRouter

from apps.booking.views import RoomViewSet, BookingViewSet, CarouselViewSet, MyBookingViewSet


router = SimpleRouter()
router.register("rooms", RoomViewSet)
router.register("booking/create", BookingViewSet)
router.register("booking", MyBookingViewSet)
router.register('carousel', CarouselViewSet)

urls = router.urls

from rest_framework.routers import SimpleRouter

from apps.booking.views import RoomViewSet, BookingViewSet, CarouselViewSet


router = SimpleRouter()
router.register("rooms", RoomViewSet)
router.register("bookings", BookingViewSet)
router.register('carousel', CarouselViewSet)

urls = router.urls

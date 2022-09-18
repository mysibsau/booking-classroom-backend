from rest_framework.routers import SimpleRouter

from apps.booking.views import RoomViewSet, BookingViewSet


router = SimpleRouter()
router.register("rooms", RoomViewSet)
router.register("bookings", BookingViewSet)


urls = router.urls

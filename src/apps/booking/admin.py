from django.contrib import admin, messages
from django.contrib.admin import TabularInline
from django.http import HttpResponseRedirect
from django.utils.html import format_html

from apps.booking.models import \
    Room, \
    Equipment, \
    EquipmentInRoom, \
    Booking, BookingDateTime, \
    RoomPhoto, \
    Carousel, \
    CarouselPhoto, \
    StaticDateTime


admin.site.site_header = "Панель администрирования"
admin.site.site_title = "Панель администрирования"
admin.site.index_title = "Добро пожаловать в панель администратора"


class CarouselAdminInline(TabularInline):
    extra = 0
    model = CarouselPhoto


class StaticDateTimeAdminInLine(TabularInline):
    extra = 0
    model = StaticDateTime


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    inlines = (CarouselAdminInline, )

    def has_add_permission(self, request):
        if request.user.role == 2:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.role == 2:
            return True
        return False


class EquipAdminInline(TabularInline):
    extra = 0
    model = EquipmentInRoom
    autocomplete_fields = ('equipment', )


class BookingDateTimeInLine(TabularInline):

    extra = 0
    model = BookingDateTime
    readonly_fields = ('date_start', 'date_end', 'start_time', 'end_time', )
    can_delete = False


class RoomPhotoInLine(TabularInline):
    extra = 0
    model = RoomPhoto


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = (EquipAdminInline, RoomPhotoInLine, StaticDateTimeAdminInLine)

    def get_queryset(self, request):
        if request.user.role == 1:
            queryset = Room.objects.all().filter(admin=request.user)
            return queryset

        return super().get_queryset(request)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'description', 'is_spec_equip', )

    def has_add_permission(self, request):
        if request.user.role == 2:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.role == 2:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.role == 2:
            return True
        return False


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    # def children_display(self, obj):
    #     return [item for item in obj.booking_date_time.all()]

    search_fields = ('room__address', )
    inlines = (BookingDateTimeInLine,)
    list_display = ('user', 'room', 'booking_status', )
    readonly_fields = ('user', 'room', 'contact_info', 'equipment', 'status', 'title', 'description', 'personal_status', 'position')
    list_filter = ('status', )
    change_form_template = "admin/booking_change_form.html"
    fields = ('user', 'room', 'contact_info', 'equipment', 'title', 'description', 'status', 'personal_status', 'position', 'comment', )
    # children_display.short_description = "Даты брони"

    def booking_status(self, obj):
        if obj.status == 0:
            return format_html('<div style="width:10; height:10; background-color:#ffc188;color:white;padding:5px;border-radius:8px;font-size:16px;font-weight:600;">В обработке</div>')
        elif obj.status == 1:
            return format_html('<div style="width:10; height:10; background-color:#ff6363;color:white;padding:5px;border-radius:8px;font-size:16px;font-weight:600;">Отклонено</div>')
        else:
            return format_html('<div style="width:10; height:10; background-color:#7dc71c;color:white;padding:5px;border-radius:8px;font-size:16px;font-weight:600;">Одобрено</div>')

    booking_status.short_description = "Статус заявки"
    booking_status.allow_tags = True

    def response_change(self, request, obj):
        if '_accept' in request.POST:
            obj.status = 2
            obj.comment = None
            obj.save()
            self.message_user(request, 'Заявка одобрена!')
            return HttpResponseRedirect("../")
        elif '_reject' in request.POST:
            if obj.comment is None or obj.comment == "":
                messages.error(request, 'Укажите причину отказа')
                return HttpResponseRedirect("../")
            obj.status = 1
            obj.save()
            self.message_user(request, 'Заявка отклонена!')
            return HttpResponseRedirect("../")

        return super().response_change(request, obj)

    def get_queryset(self, request):
        if request.user.role == 1:
            queryset = Booking.objects.all().filter(room__admin=request.user)
            return queryset

        return super().get_queryset(request)

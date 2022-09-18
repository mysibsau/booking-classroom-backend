from django.contrib import admin, messages
from django.contrib.admin import TabularInline
from django.http import HttpResponseRedirect
from django.utils.html import format_html

from apps.booking.models import Room, Equipment, EquipmentInRoom, Booking, BookingDateTime, RoomPhoto


admin.site.site_header = "Панель администрирования"
admin.site.site_title = "Панель администрирования"
admin.site.index_title = "Добро пожаловать в панель администратора"


class EquipAdminInline(TabularInline):
    extra = 0
    model = EquipmentInRoom
    autocomplete_fields = ('equipment', )


class BookingDateTimeInLine(TabularInline):

    extra = 0
    model = BookingDateTime
    readonly_fields = ('date', 'start_time', 'end_time', )
    can_delete = False


class RoomPhotoInLine(TabularInline):
    extra = 0
    model = RoomPhoto


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = (EquipAdminInline, RoomPhotoInLine)

    def get_queryset(self, request):
        if request.user.role == 1:
            queryset = Room.objects.all().filter(admin=request.user)
            return queryset

        return super().get_queryset(request)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'description', )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    search_fields = ('room__address', )
    inlines = (BookingDateTimeInLine,)
    list_display = ('user', 'room', 'booking_status', )
    readonly_fields = ('user', 'room', 'contact_info', 'equipment', 'status', 'description')
    list_filter = ('status', )
    change_form_template = "admin/booking_change_form.html"
    fields = ('user', 'room', 'contact_info', 'equipment', 'description', 'status', 'comment')

    def booking_status(self, obj):
        if obj.status == 0:
            return format_html('<div style="width:10; height:10; background-color:yellow;">В обработке</div>')
        elif obj.status == 1:
            return format_html('<div style="width:10; height:10; background-color:green;">Одобрено</div>')

        return format_html('<div style="width:10; height:10; background-color:red;">Отклонено</div>')

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

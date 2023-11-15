from django.contrib import admin, messages
from django.contrib.admin import TabularInline, DateFieldListFilter
from django.http import HttpResponseRedirect
from django.utils import timezone
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
        if request.user.role == 2:
            return True
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
    autocomplete_fields = ('admin', 'pseudo_admins')
    search_fields = ('address', )
    inlines = (EquipAdminInline, RoomPhotoInLine, StaticDateTimeAdminInLine)
    fields = ('admin', 'pseudo_admins', 'admin_contact_info', 'address', 'description', 'capacity')

    def get_queryset(self, request):
        if request.user.role == 2:
            return super().get_queryset(request)
        elif request.user.role == 3:
            queryset = Room.objects.all().filter(pseudo_admins=request.user)
            return queryset
        queryset = Room.objects.all().filter(admin=request.user)
        return queryset

    def get_readonly_fields(self, request, obj=None):
        if request.user.role == 2:
            return super(RoomAdmin, self).get_readonly_fields(request, obj)
        return 'admin', 'pseudo_admins'


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


class CustomDateFieldFilter(DateFieldListFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = timezone.now()
        self.links = (
            ('Любая дата', {}),
            ('Сегодня', {'{}__gte'.format(self.field_path): now.date().strftime('%Y-%m-%d'),
                         '{}__lt'.format(self.field_path): (now.date() + timezone.timedelta(days=1)).strftime('%Y-%m-%d')}),
            ('Завтра', {'{}__gte'.format(self.field_path): (now.date() + timezone.timedelta(days=1)).strftime('%Y-%m-%d'),
                        '{}__lt'.format(self.field_path): (now.date() + timezone.timedelta(days=2)).strftime('%Y-%m-%d')}),
            ('Предстоящие 7 дней', {'{}__gte'.format(self.field_path): (now.date() + timezone.timedelta(days=1)).strftime('%Y-%m-%d'),
                                    '{}__lt'.format(self.field_path): (now.date() + timezone.timedelta(days=7)).strftime('%Y-%m-%d')}),
        )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    def booking_date_time_display(self, obj):
        return obj.booking_date_time.first()

    search_fields = ('room__address', 'user__full_name', 'booking_date_time__date_start')
    inlines = (BookingDateTimeInLine,)
    list_display = ('user', 'room', 'booking_date_time_display', 'booking_status', )
    readonly_fields = ('created_at', 'user', 'room', 'contact_info', 'equipment', 'status', 'title', 'description', 'personal_status', 'position')
    list_filter = ('status', ('booking_date_time__date_start', CustomDateFieldFilter), )
    change_form_template = "admin/booking_change_form.html"
    fields = ('created_at', 'user', 'room', 'contact_info', 'equipment', 'title', 'description', 'status', 'personal_status', 'position', 'comment', )
    booking_date_time_display.short_description = "Даты и время брони"
    # ordering = ('booking_date_time__date_start',)

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
        elif request.user.role == 3:
            queryset = Booking.objects.all().filter(room__pseudo_admins=request.user, status=2)
            return queryset
        return super().get_queryset(request)

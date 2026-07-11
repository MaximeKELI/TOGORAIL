from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import ContactMessage, PartnerLogo, Service, Stat, TimelineEvent


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title_fr", "title_en", "icon", "order", "featured")
    list_editable = ("order", "featured")
    search_fields = ("title_fr", "title_en")


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ("label_fr", "value", "suffix", "order")
    list_editable = ("value", "suffix", "order")


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ("year", "title_fr", "order")
    list_editable = ("order",)


@admin.register(PartnerLogo)
class PartnerLogoAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "subject", "created_at", "handled")
    list_filter = ("handled", "created_at")
    search_fields = ("name", "email", "company", "message")
    list_editable = ("handled",)
    readonly_fields = ("created_at",)

    @admin.action(description=_("Marquer comme traité"))
    def mark_handled(self, request, queryset):
        queryset.update(handled=True)

    actions = ["mark_handled"]


admin.site.site_header = "Togo Rail — Administration"
admin.site.site_title = "Togo Rail"
admin.site.index_title = _("Gestion du contenu")

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    Article,
    ContactMessage,
    FAQ,
    JobApplication,
    JobOffer,
    PartnerLogo,
    Project,
    Service,
    Stat,
    Subscriber,
    Testimonial,
    TimelineEvent,
)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title_fr", "title_en", "icon", "order", "featured")
    list_editable = ("order", "featured")
    search_fields = ("title_fr", "title_en")
    prepopulated_fields = {"slug": ("title_en",)}


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
    list_display = ("name", "email", "user", "company", "subject", "created_at", "handled")
    list_filter = ("handled", "created_at")
    search_fields = ("name", "email", "company", "message", "user__username")
    autocomplete_fields = ("user",)
    list_editable = ("handled",)
    readonly_fields = ("created_at",)

    @admin.action(description=_("Marquer comme traité"))
    def mark_handled(self, request, queryset):
        queryset.update(handled=True)

    actions = ["mark_handled"]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title_fr", "category_fr", "published_at", "is_published")
    list_filter = ("is_published", "category_fr", "published_at")
    list_editable = ("is_published",)
    search_fields = ("title_fr", "title_en", "body_fr", "body_en")
    prepopulated_fields = {"slug": ("title_en",)}
    date_hierarchy = "published_at"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title_fr", "year", "location", "order")
    list_editable = ("order",)
    search_fields = ("title_fr", "title_en")
    prepopulated_fields = {"slug": ("title_en",)}


@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = ("title_fr", "location", "contract_type", "is_open", "order")
    list_editable = ("is_open", "order")
    list_filter = ("is_open", "contract_type")
    search_fields = ("title_fr", "title_en")


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "offer", "created_at")
    list_filter = ("created_at", "offer")
    search_fields = ("name", "email")
    readonly_fields = ("created_at",)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question_fr", "order")
    list_editable = ("order",)
    search_fields = ("question_fr", "question_en")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author", "role_fr", "order")
    list_editable = ("order",)
    search_fields = ("author", "quote_fr", "quote_en")


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at")
    search_fields = ("email",)
    readonly_fields = ("created_at",)


admin.site.site_header = "Togo Rail — Administration"
admin.site.site_title = "Togo Rail"
admin.site.index_title = _("Gestion du contenu")

from django.db import models
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _


class LocalizedMixin:
    """Return the field matching the active language, falling back to FR."""

    def localized(self, field: str) -> str:
        lang = (get_language() or "fr")[:2]
        value = getattr(self, f"{field}_{lang}", "") or getattr(self, f"{field}_fr", "")
        return value


class Service(LocalizedMixin, models.Model):
    title_fr = models.CharField(_("Titre (FR)"), max_length=120)
    title_en = models.CharField(_("Title (EN)"), max_length=120)
    summary_fr = models.TextField(_("Résumé (FR)"))
    summary_en = models.TextField(_("Summary (EN)"))
    # Inline SVG path data or an emoji/icon key rendered by the template.
    icon = models.CharField(
        _("Icône (nom)"),
        max_length=40,
        default="rail",
        help_text=_("rail, cargo, network, shield, bolt, globe"),
    )
    order = models.PositiveIntegerField(_("Ordre"), default=0)
    featured = models.BooleanField(_("Mis en avant"), default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self):
        return self.title_fr

    @property
    def title(self):
        return self.localized("title")

    @property
    def summary(self):
        return self.localized("summary")


class Stat(LocalizedMixin, models.Model):
    label_fr = models.CharField(_("Libellé (FR)"), max_length=80)
    label_en = models.CharField(_("Label (EN)"), max_length=80)
    value = models.PositiveIntegerField(_("Valeur"))
    suffix = models.CharField(_("Suffixe"), max_length=8, blank=True, default="")
    prefix = models.CharField(_("Préfixe"), max_length=8, blank=True, default="")
    order = models.PositiveIntegerField(_("Ordre"), default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Statistique")
        verbose_name_plural = _("Statistiques")

    def __str__(self):
        return f"{self.value}{self.suffix} — {self.label_fr}"

    @property
    def label(self):
        return self.localized("label")


class TimelineEvent(LocalizedMixin, models.Model):
    year = models.CharField(_("Année"), max_length=12)
    title_fr = models.CharField(_("Titre (FR)"), max_length=120)
    title_en = models.CharField(_("Title (EN)"), max_length=120)
    body_fr = models.TextField(_("Description (FR)"))
    body_en = models.TextField(_("Description (EN)"))
    order = models.PositiveIntegerField(_("Ordre"), default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Étape (timeline)")
        verbose_name_plural = _("Timeline")

    def __str__(self):
        return f"{self.year} — {self.title_fr}"

    @property
    def title(self):
        return self.localized("title")

    @property
    def body(self):
        return self.localized("body")


class PartnerLogo(models.Model):
    name = models.CharField(_("Nom"), max_length=80)
    image = models.ImageField(_("Logo"), upload_to="logos/", blank=True, null=True)
    url = models.URLField(_("Lien"), blank=True, default="")
    order = models.PositiveIntegerField(_("Ordre"), default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Logo partenaire")
        verbose_name_plural = _("Logos partenaires")

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(_("Nom"), max_length=120)
    email = models.EmailField(_("Email"))
    company = models.CharField(_("Société"), max_length=120, blank=True, default="")
    subject = models.CharField(_("Sujet"), max_length=160, blank=True, default="")
    message = models.TextField(_("Message"))
    created_at = models.DateTimeField(_("Reçu le"), auto_now_add=True)
    handled = models.BooleanField(_("Traité"), default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Message de contact")
        verbose_name_plural = _("Messages de contact")

    def __str__(self):
        return f"{self.name} — {self.email}"

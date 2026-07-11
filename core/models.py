from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
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
    slug = models.SlugField(_("Slug"), max_length=140, blank=True, unique=True)
    summary_fr = models.TextField(_("Résumé (FR)"))
    summary_en = models.TextField(_("Summary (EN)"))
    body_fr = models.TextField(_("Description détaillée (FR)"), blank=True, default="")
    body_en = models.TextField(_("Detailed description (EN)"), blank=True, default="")
    image = models.ImageField(_("Image"), upload_to="services/", blank=True, null=True)
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en or self.title_fr)[:140]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("service_detail", args=[self.slug])

    @property
    def title(self):
        return self.localized("title")

    @property
    def summary(self):
        return self.localized("summary")

    @property
    def body(self):
        return self.localized("body")


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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages",
        verbose_name=_("Utilisateur"),
    )
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


class Article(LocalizedMixin, models.Model):
    title_fr = models.CharField(_("Titre (FR)"), max_length=160)
    title_en = models.CharField(_("Title (EN)"), max_length=160)
    slug = models.SlugField(_("Slug"), max_length=180, blank=True, unique=True)
    excerpt_fr = models.TextField(_("Chapô (FR)"))
    excerpt_en = models.TextField(_("Excerpt (EN)"))
    body_fr = models.TextField(_("Contenu (FR)"))
    body_en = models.TextField(_("Content (EN)"))
    cover = models.ImageField(_("Image de couverture"), upload_to="blog/", blank=True, null=True)
    category_fr = models.CharField(_("Catégorie (FR)"), max_length=60, blank=True, default="Actualité")
    category_en = models.CharField(_("Category (EN)"), max_length=60, blank=True, default="News")
    published_at = models.DateTimeField(_("Date de publication"))
    is_published = models.BooleanField(_("Publié"), default=True)

    class Meta:
        ordering = ["-published_at"]
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    def __str__(self):
        return self.title_fr

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en or self.title_fr)[:180]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("article_detail", args=[self.slug])

    @property
    def title(self):
        return self.localized("title")

    @property
    def excerpt(self):
        return self.localized("excerpt")

    @property
    def body(self):
        return self.localized("body")

    @property
    def category(self):
        return self.localized("category")


class Project(LocalizedMixin, models.Model):
    title_fr = models.CharField(_("Titre (FR)"), max_length=160)
    title_en = models.CharField(_("Title (EN)"), max_length=160)
    slug = models.SlugField(_("Slug"), max_length=180, blank=True, unique=True)
    summary_fr = models.TextField(_("Résumé (FR)"))
    summary_en = models.TextField(_("Summary (EN)"))
    body_fr = models.TextField(_("Étude de cas (FR)"), blank=True, default="")
    body_en = models.TextField(_("Case study (EN)"), blank=True, default="")
    image = models.ImageField(_("Image"), upload_to="projects/", blank=True, null=True)
    year = models.CharField(_("Année"), max_length=12, blank=True, default="")
    location = models.CharField(_("Lieu"), max_length=120, blank=True, default="")
    order = models.PositiveIntegerField(_("Ordre"), default=0)

    class Meta:
        ordering = ["order", "-year"]
        verbose_name = _("Projet")
        verbose_name_plural = _("Projets")

    def __str__(self):
        return self.title_fr

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en or self.title_fr)[:180]
        super().save(*args, **kwargs)

    @property
    def title(self):
        return self.localized("title")

    @property
    def summary(self):
        return self.localized("summary")

    @property
    def body(self):
        return self.localized("body")


class JobOffer(LocalizedMixin, models.Model):
    CONTRACT_CHOICES = [
        ("cdi", _("CDI")),
        ("cdd", _("CDD")),
        ("stage", _("Stage")),
        ("alternance", _("Alternance")),
    ]
    title_fr = models.CharField(_("Poste (FR)"), max_length=160)
    title_en = models.CharField(_("Position (EN)"), max_length=160)
    location = models.CharField(_("Lieu"), max_length=120, default="Lomé, Togo")
    contract_type = models.CharField(_("Contrat"), max_length=20, choices=CONTRACT_CHOICES, default="cdi")
    description_fr = models.TextField(_("Description (FR)"))
    description_en = models.TextField(_("Description (EN)"))
    is_open = models.BooleanField(_("Ouvert"), default=True)
    order = models.PositiveIntegerField(_("Ordre"), default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Offre d'emploi")
        verbose_name_plural = _("Offres d'emploi")

    def __str__(self):
        return self.title_fr

    @property
    def title(self):
        return self.localized("title")

    @property
    def description(self):
        return self.localized("description")


class JobApplication(models.Model):
    offer = models.ForeignKey(
        JobOffer, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="applications", verbose_name=_("Offre"),
    )
    name = models.CharField(_("Nom"), max_length=120)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Téléphone"), max_length=40, blank=True, default="")
    cv = models.FileField(_("CV"), upload_to="cv/")
    message = models.TextField(_("Message"), blank=True, default="")
    created_at = models.DateTimeField(_("Reçu le"), auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Candidature")
        verbose_name_plural = _("Candidatures")

    def __str__(self):
        return f"{self.name} — {self.email}"


class FAQ(LocalizedMixin, models.Model):
    question_fr = models.CharField(_("Question (FR)"), max_length=200)
    question_en = models.CharField(_("Question (EN)"), max_length=200)
    answer_fr = models.TextField(_("Réponse (FR)"))
    answer_en = models.TextField(_("Answer (EN)"))
    order = models.PositiveIntegerField(_("Ordre"), default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQ")

    def __str__(self):
        return self.question_fr

    @property
    def question(self):
        return self.localized("question")

    @property
    def answer(self):
        return self.localized("answer")


class Testimonial(LocalizedMixin, models.Model):
    author = models.CharField(_("Auteur"), max_length=120)
    role_fr = models.CharField(_("Fonction (FR)"), max_length=120)
    role_en = models.CharField(_("Role (EN)"), max_length=120)
    quote_fr = models.TextField(_("Citation (FR)"))
    quote_en = models.TextField(_("Quote (EN)"))
    avatar = models.ImageField(_("Photo"), upload_to="testimonials/", blank=True, null=True)
    order = models.PositiveIntegerField(_("Ordre"), default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Témoignage")
        verbose_name_plural = _("Témoignages")

    def __str__(self):
        return self.author

    @property
    def role(self):
        return self.localized("role")

    @property
    def quote(self):
        return self.localized("quote")


class Subscriber(models.Model):
    email = models.EmailField(_("Email"), unique=True)
    created_at = models.DateTimeField(_("Inscrit le"), auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Abonné newsletter")
        verbose_name_plural = _("Abonnés newsletter")

    def __str__(self):
        return self.email

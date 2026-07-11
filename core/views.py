from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from .forms import (
    ContactForm,
    JobApplicationForm,
    LoginForm,
    MemberMessageForm,
    NewsletterForm,
    SignUpForm,
)
from .models import (
    Article,
    FAQ,
    JobOffer,
    PartnerLogo,
    Project,
    Service,
    Stat,
    Subscriber,
    Testimonial,
    TimelineEvent,
)


def _common():
    return {
        "services": Service.objects.all(),
        "stats": Stat.objects.all(),
        "timeline": TimelineEvent.objects.all(),
        "partners": PartnerLogo.objects.all(),
        "testimonials": Testimonial.objects.all(),
        "faqs": FAQ.objects.all(),
        "newsletter_form": NewsletterForm(),
    }


def _rate_limited(request, key: str, limit: int = 30, window: int = 300) -> bool:
    """Simple IP-based rate limiter backed by the cache.

    Uses a short window so any accidental lockout clears quickly, and a
    generous limit so legitimate users (including failed form validations)
    are never blocked during normal use.
    """
    ip = request.META.get("REMOTE_ADDR", "unknown")
    cache_key = f"rl:{key}:{ip}"
    count = cache.get(cache_key, 0)
    if count >= limit:
        return True
    cache.set(cache_key, count + 1, window)
    return False


def home(request):
    ctx = _common()
    ctx["featured_services"] = ctx["services"].filter(featured=True)[:6]
    ctx["projects"] = Project.objects.all()[:6]
    ctx["articles"] = Article.objects.filter(is_published=True)[:3]
    ctx["active_page"] = "home"
    ctx["meta_description"] = _(
        "Togo Rail conçoit et exploite des infrastructures ferroviaires de nouvelle "
        "génération pour connecter l'Afrique de l'Ouest."
    )
    return render(request, "pages/home.html", ctx)


def about(request):
    ctx = _common()
    ctx["active_page"] = "about"
    ctx["meta_description"] = _(
        "Découvrez la mission, la vision et l'histoire de Togo Rail."
    )
    return render(request, "pages/about.html", ctx)


def services(request):
    ctx = _common()
    ctx["active_page"] = "services"
    ctx["meta_description"] = _(
        "Fret, transport de passagers, ingénierie et maintenance : l'offre complète de Togo Rail."
    )
    return render(request, "pages/services.html", ctx)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    ctx = _common()
    ctx["service"] = service
    ctx["other_services"] = Service.objects.exclude(pk=service.pk)[:3]
    ctx["active_page"] = "services"
    ctx["meta_description"] = service.summary
    return render(request, "pages/service_detail.html", ctx)


def projects(request):
    ctx = _common()
    ctx["projects"] = Project.objects.all()
    ctx["active_page"] = "projects"
    ctx["meta_description"] = _("Nos réalisations et études de cas ferroviaires.")
    return render(request, "pages/projects.html", ctx)


def blog(request):
    ctx = _common()
    ctx["articles"] = Article.objects.filter(is_published=True)
    ctx["active_page"] = "blog"
    ctx["meta_description"] = _("Actualités, annonces et publications de Togo Rail.")
    return render(request, "pages/blog.html", ctx)


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    ctx = _common()
    ctx["article"] = article
    ctx["related"] = Article.objects.filter(is_published=True).exclude(pk=article.pk)[:3]
    ctx["active_page"] = "blog"
    ctx["meta_description"] = article.excerpt
    return render(request, "pages/article_detail.html", ctx)


def careers(request):
    ctx = _common()
    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES)
        if _rate_limited(request, "apply", limit=5):
            messages.error(request, _("Trop de tentatives. Réessayez plus tard."))
        elif form.is_valid():
            application = form.save()
            _notify_application(application)
            messages.success(
                request,
                _("Merci ! Votre candidature a bien été reçue."),
            )
            return redirect("careers")
        else:
            messages.error(request, _("Veuillez corriger les erreurs ci-dessous."))
    else:
        form = JobApplicationForm()

    ctx["offers"] = JobOffer.objects.filter(is_open=True)
    ctx["form"] = form
    ctx["active_page"] = "careers"
    ctx["meta_description"] = _("Rejoignez les équipes de Togo Rail.")
    return render(request, "pages/careers.html", ctx)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if _rate_limited(request, "contact", limit=5):
            messages.error(request, _("Trop de messages envoyés. Réessayez plus tard."))
        elif form.is_valid():
            msg = form.save(commit=False)
            if request.user.is_authenticated:
                msg.user = request.user
            msg.save()
            _notify_contact(msg)
            messages.success(
                request,
                _("Merci ! Votre message a bien été envoyé. Nous vous répondrons rapidement."),
            )
            return redirect("contact")
        else:
            messages.error(request, _("Veuillez corriger les erreurs ci-dessous."))
    else:
        form = ContactForm()

    ctx = _common()
    ctx["form"] = form
    ctx["active_page"] = "contact"
    ctx["meta_description"] = _("Contactez les équipes de Togo Rail.")
    return render(request, "pages/contact.html", ctx)


@require_POST
def newsletter_subscribe(request):
    email = (request.POST.get("email") or "").strip().lower()
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"
    form = NewsletterForm({"email": email})
    if _rate_limited(request, "newsletter", limit=10):
        msg = _("Trop de tentatives. Réessayez plus tard.")
        ok = False
    elif form.is_valid():
        Subscriber.objects.get_or_create(email=email)
        msg = _("Merci ! Vous êtes bien inscrit à notre newsletter.")
        ok = True
    else:
        msg = _("Adresse e-mail invalide.")
        ok = False

    if is_ajax:
        return JsonResponse({"ok": ok, "message": str(msg)})
    messages.success(request, msg) if ok else messages.error(request, msg)
    return redirect(request.META.get("HTTP_REFERER", "home"))


def faq(request):
    ctx = _common()
    ctx["active_page"] = "faq"
    ctx["meta_description"] = _("Questions fréquentes à propos de Togo Rail.")
    return render(request, "pages/faq.html", ctx)


# ── Authentication & member area ──────────────────────────────────────────

def register(request):
    if request.user.is_authenticated:
        return redirect("account")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if _rate_limited(request, "register", limit=8):
            messages.error(request, _("Trop de tentatives. Réessayez plus tard."))
        elif form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, _("Bienvenue ! Votre compte a bien été créé."))
            return redirect("account")
        else:
            messages.error(request, _("Veuillez corriger les erreurs ci-dessous."))
    else:
        form = SignUpForm()
    ctx = _common()
    ctx["form"] = form
    ctx["active_page"] = "register"
    ctx["meta_description"] = _("Créez votre compte Togo Rail.")
    return render(request, "pages/register.html", ctx)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("account")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.success(request, _("Connexion réussie."))
            nxt = request.GET.get("next") or request.POST.get("next")
            return redirect(nxt or "account")
        messages.error(request, _("Identifiants invalides."))
    else:
        form = LoginForm(request)
    ctx = _common()
    ctx["form"] = form
    ctx["active_page"] = "login"
    ctx["next"] = request.GET.get("next", "")
    ctx["meta_description"] = _("Connectez-vous à votre espace Togo Rail.")
    return render(request, "pages/login.html", ctx)


@require_POST
def logout_view(request):
    auth_logout(request)
    messages.success(request, _("Vous êtes déconnecté."))
    return redirect("home")


@login_required
def account(request):
    if request.method == "POST":
        form = MemberMessageForm(request.POST)
        if _rate_limited(request, "member_msg", limit=10):
            messages.error(request, _("Trop de messages envoyés. Réessayez plus tard."))
        elif form.is_valid():
            msg = form.save(commit=False)
            msg.user = request.user
            msg.name = request.user.get_full_name() or request.user.username
            msg.email = request.user.email
            msg.save()
            _notify_contact(msg)
            messages.success(request, _("Message envoyé à Togo Rail. Merci !"))
            return redirect("account")
        else:
            messages.error(request, _("Veuillez corriger les erreurs ci-dessous."))
    else:
        form = MemberMessageForm()

    ctx = _common()
    ctx["form"] = form
    ctx["my_messages"] = request.user.messages.all()
    ctx["active_page"] = "account"
    ctx["meta_description"] = _("Votre espace membre Togo Rail.")
    return render(request, "pages/account.html", ctx)


# ── Email helpers ─────────────────────────────────────────────────────────

def _notify_contact(msg):
    try:
        send_mail(
            subject=f"[Togo Rail] Nouveau message — {msg.subject or msg.name}",
            message=(
                f"De : {msg.name} <{msg.email}>\n"
                f"Société : {msg.company}\n\n{msg.message}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=True,
        )
        # Auto-acknowledgement to the sender.
        send_mail(
            subject=_("Togo Rail — Nous avons bien reçu votre message"),
            message=_(
                "Bonjour %(name)s,\n\nMerci de nous avoir contactés. "
                "Notre équipe vous répondra dans les meilleurs délais.\n\n— Togo Rail"
            ) % {"name": msg.name},
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[msg.email],
            fail_silently=True,
        )
    except Exception:
        pass


def _notify_application(application):
    try:
        send_mail(
            subject=f"[Togo Rail] Candidature — {application.name}",
            message=(
                f"Candidat : {application.name} <{application.email}>\n"
                f"Poste : {application.offer}\n"
                f"Téléphone : {application.phone}\n\n{application.message}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=True,
        )
    except Exception:
        pass

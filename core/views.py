from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from .forms import ContactForm
from .models import PartnerLogo, Service, Stat, TimelineEvent


def _common():
    return {
        "services": Service.objects.all(),
        "stats": Stat.objects.all(),
        "timeline": TimelineEvent.objects.all(),
        "partners": PartnerLogo.objects.all(),
    }


def home(request):
    ctx = _common()
    ctx["featured_services"] = ctx["services"].filter(featured=True)[:6]
    ctx["active_page"] = "home"
    return render(request, "pages/home.html", ctx)


def about(request):
    ctx = _common()
    ctx["active_page"] = "about"
    return render(request, "pages/about.html", ctx)


def services(request):
    ctx = _common()
    ctx["active_page"] = "services"
    return render(request, "pages/services.html", ctx)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                _("Merci ! Votre message a bien été envoyé. Nous vous répondrons rapidement."),
            )
            return redirect("contact")
        messages.error(request, _("Veuillez corriger les erreurs ci-dessous."))
    else:
        form = ContactForm()

    ctx = _common()
    ctx["form"] = form
    ctx["active_page"] = "contact"
    return render(request, "pages/contact.html", ctx)

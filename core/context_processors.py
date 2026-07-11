from django.utils.translation import gettext_lazy as _


def site_globals(request):
    """Global values available to every template."""
    return {
        "SITE_NAME": "Togo Rail",
        "SITE_TAGLINE": _("Relier le Togo, connecter l'Afrique de l'Ouest."),
        "CONTACT_EMAIL": "contact@togorail.tg",
        "CONTACT_PHONE": "+228 22 00 00 00",
        "CONTACT_ADDRESS": "Boulevard du Mono, Lomé, Togo",
    }

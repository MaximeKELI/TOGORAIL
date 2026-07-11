from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ContactMessage

INPUT_CLASS = (
    "peer w-full bg-white/[0.03] border border-white/10 rounded-xl px-4 py-3.5 "
    "text-white placeholder-transparent outline-none transition-all duration-300 "
    "focus:border-gold/70 focus:bg-white/[0.06] focus:ring-2 focus:ring-gold/20"
)


class ContactForm(forms.ModelForm):
    # Honeypot to deter bots (hidden via CSS).
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "company", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": " "}),
            "email": forms.EmailInput(attrs={"class": INPUT_CLASS, "placeholder": " "}),
            "company": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": " "}),
            "subject": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": " "}),
            "message": forms.Textarea(
                attrs={"class": INPUT_CLASS, "placeholder": " ", "rows": 5}
            ),
        }
        labels = {
            "name": _("Nom complet"),
            "email": _("Adresse e-mail"),
            "company": _("Société"),
            "subject": _("Sujet"),
            "message": _("Votre message"),
        }

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam detected.")
        return ""

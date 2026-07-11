from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import ContactMessage, JobApplication, Subscriber

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


class JobApplicationForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = JobApplication
        fields = ["offer", "name", "email", "phone", "cv", "message"]
        widgets = {
            "offer": forms.Select(attrs={"class": INPUT_CLASS}),
            "name": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": " "}),
            "email": forms.EmailInput(attrs={"class": INPUT_CLASS, "placeholder": " "}),
            "phone": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": " "}),
            "cv": forms.ClearableFileInput(
                attrs={
                    "class": "block w-full text-sm text-muted file:mr-4 file:py-2.5 "
                    "file:px-5 file:rounded-full file:border-0 file:bg-gold "
                    "file:text-navy file:font-semibold hover:file:bg-goldsoft "
                    "file:cursor-pointer cursor-pointer",
                    "accept": ".pdf,.doc,.docx",
                }
            ),
            "message": forms.Textarea(
                attrs={"class": INPUT_CLASS, "placeholder": " ", "rows": 4}
            ),
        }
        labels = {
            "offer": _("Poste visé"),
            "name": _("Nom complet"),
            "email": _("Adresse e-mail"),
            "phone": _("Téléphone"),
            "cv": _("CV (PDF, DOC)"),
            "message": _("Message / motivation"),
        }

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam detected.")
        return ""

    def clean_cv(self):
        cv = self.cleaned_data.get("cv")
        if cv:
            valid = (".pdf", ".doc", ".docx")
            if not cv.name.lower().endswith(valid):
                raise forms.ValidationError(_("Format accepté : PDF, DOC, DOCX."))
            if cv.size > 5 * 1024 * 1024:
                raise forms.ValidationError(_("Fichier trop volumineux (5 Mo max)."))
        return cv


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full bg-white/[0.04] border border-white/10 rounded-full "
                    "px-5 py-3 text-white placeholder-muted outline-none transition-all "
                    "duration-300 focus:border-gold/70 focus:ring-2 focus:ring-gold/20",
                    "placeholder": _("Votre e-mail"),
                }
            ),
        }
        labels = {"email": _("E-mail")}

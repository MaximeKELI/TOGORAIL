# Togo Rail — Site vitrine premium (bilingue FR / EN)

Site corporate ultra-premium pour une compagnie ferroviaire / logistique.
Thème sombre luxe, accents or, glassmorphism, animations cinématiques GSAP +
ScrollTrigger + Lenis. Contenu géré via l'admin Django, bilingue français /
anglais.

Premium bilingual (FR/EN) corporate website for a railway / logistics company.
Dark luxury theme, gold accents, glassmorphism, cinematic GSAP animations.
Content managed through the Django admin.

---

## Stack

- **Backend** : Django 5.2, PostgreSQL (SQLite en fallback local), Django ORM, Django Admin
- **Frontend** : HTML5, Tailwind CSS (Play CDN + thème custom), JavaScript ES6+
- **Animations** : GSAP 3, ScrollTrigger, Lenis (smooth scroll)
- **i18n** : `django.middleware.locale`, catalogues `locale/fr` & `locale/en`

## Structure

```
config/          # Projet Django (settings, urls, wsgi/asgi)
core/            # App principale (models, views, forms, admin, i18n)
  management/commands/seed_demo.py   # Données de démo bilingues
templates/       # base.html, partials/ (navbar, footer, icon), pages/
static/
  css/styles.css # Design system (glass, glow, boutons, timeline, form)
  js/main.js     # Lenis, navbar, menu mobile, toasts, glow cartes
  js/animations.js # GSAP: hero timeline, reveals, counters, marquee
  media/hero-poster.svg
locale/{fr,en}/  # Traductions .po / .mo
```

## Démarrage rapide (local, SQLite)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env            # DB_ENGINE=sqlite par défaut
python manage.py migrate
python manage.py seed_demo      # contenu de démonstration
python manage.py createsuperuser
python manage.py runserver
```

Ouvrir http://127.0.0.1:8000/ (redirige vers `/fr/`). Admin : `/admin/`.

## Passer en PostgreSQL (production)

1. Créer la base et l'utilisateur :

```sql
CREATE DATABASE togo_rail;
CREATE USER togo WITH PASSWORD 'motdepasse';
GRANT ALL PRIVILEGES ON DATABASE togo_rail TO togo;
```

2. Dans `.env` :

```
DB_ENGINE=postgres
DB_NAME=togo_rail
DB_USER=togo
DB_PASSWORD=motdepasse
DB_HOST=127.0.0.1
DB_PORT=5432
```

3. `python manage.py migrate && python manage.py seed_demo`

## Bilingue (FR / EN)

- Langue par défaut : **français**. URLs préfixées : `/fr/...`, `/en/...`.
- Sélecteur de langue dans la navbar (endpoint `set_language`).
- Textes d'interface : balises `{% trans %}` → catalogues `locale/`.
- Contenu éditorial (services, stats, timeline) : champs `_fr` / `_en` sur les
  modèles, résolus automatiquement selon la langue active.

Regénérer / recompiler les traductions après modification des templates :

```bash
python manage.py makemessages -l fr -l en --ignore=venv
# éditer locale/en/LC_MESSAGES/django.po
python manage.py compilemessages -l fr -l en
```

## Gestion du contenu (Admin)

Modèles éditables : `Service`, `Stat`, `TimelineEvent`, `PartnerLogo`,
`ContactMessage`. Les messages du formulaire de contact arrivent dans
« Messages de contact ».

## Médias hero

`static/media/hero-poster.svg` sert de poster / fallback. Pour une vidéo réelle,
déposer `static/media/hero.mp4` (le `<video>` la chargera automatiquement).

## Production

- `DEBUG=False`, renseigner `SECRET_KEY` et `ALLOWED_HOSTS`.
- `python manage.py collectstatic` (WhiteNoise sert les statiques compressés).
- Servir via `gunicorn config.wsgi:application`.
- Pour un vrai build Tailwind (au lieu du CDN Play), ajouter un pipeline Node
  (`tailwindcss` CLI) et remplacer le `<script src="cdn.tailwindcss.com">`.
```

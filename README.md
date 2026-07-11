# Togo Rail — Site vitrine premium (bilingue FR / EN)

Site corporate ultra-premium pour une compagnie ferroviaire / logistique.
Thème sombre luxe (+ mode clair), accents or, glassmorphism, animations
cinématiques GSAP + ScrollTrigger, particules Three.js. Contenu géré via
l'admin Django, entièrement bilingue français / anglais.

Premium bilingual (FR/EN) corporate website for a railway / logistics company.
Dark luxury theme (with light mode), gold accents, glassmorphism, cinematic
GSAP animations, Three.js hero particles. Content managed through the Django admin.

---

## Stack

- **Backend** : Django 5.x, PostgreSQL (SQLite en fallback local), Django ORM/Admin, Sitemaps
- **Frontend** : HTML5, Tailwind CSS (Play CDN + build CLI optionnel), JavaScript ES6+
- **Animations** : GSAP 3, ScrollTrigger, ScrollToPlugin, Three.js
- **i18n** : `django.middleware.locale`, catalogues `locale/fr` & `locale/en`
- **Déploiement** : Dockerfile + docker-compose (PostgreSQL), gunicorn, WhiteNoise

## Fonctionnalités

**Pages** : Accueil, Services + **détail par service** (`/services/<slug>/`),
**Réalisations** (études de cas), **Actualités / Blog** + article, **Carrières**
(+ formulaire de candidature avec upload CV), **FAQ** (accordéon animé), À propos,
Contact.

**Backend** : envoi d'e-mails sur message de contact + **accusé de réception
automatique**, **newsletter** (AJAX, modèle `Subscriber`), anti-spam (honeypot +
**rate-limiting** par IP), **sitemap.xml** + **robots.txt**, méta **SEO / Open
Graph / Twitter** dynamiques, favicon SVG.

**Expérience premium** : particules **Three.js** dans le hero, reveals de titres
**lettre par lettre** (préservant les dégradés), **transitions de page** (voile
doré), **préchargeur** avec tracé SVG animé, **curseur contextuel** (« Voir »,
« Lire », « Explorer »), cartes 3D tilt, marquee réactif à la vitesse de scroll,
scroll horizontal épinglé, typographie cinétique, **témoignages** en slider,
**mode clair / sombre** persistant, **indicateur de section active** dans la
navbar, **images WebP** avec fallback `<picture>`, accessibilité (focus visible,
`aria`, `prefers-reduced-motion`).

## Structure

```
config/          # Projet Django (settings, urls, wsgi/asgi, sitemaps)
core/            # App principale (models, views, forms, admin, sitemaps, i18n)
  management/commands/seed_demo.py        # Données de démo bilingues
  management/commands/optimize_images.py  # Génère les WebP depuis les PNG/JPG
templates/       # base.html, partials/, pages/ (home, services, service_detail,
                 #   projects, blog, article_detail, careers, faq, about, contact)
static/
  css/styles.css          # Design system complet
  css/tailwind.input.css  # Entrée pour build Tailwind CLI (optionnel)
  js/main.js       # navbar, menu, toasts, thème, section active, newsletter AJAX
  js/animations.js # GSAP: hero timeline, reveals, counters, marquee, timeline
  js/premium.js    # préchargeur, curseur, tilt, split-text, transitions, accordéon, slider
  js/lights.js     # canvas particules/god-rays hero
  js/hero3d.js     # champ de particules Three.js
  js/carousel.js   # carrousel media hero
  media/*.png *.webp *.mp4 favicon.svg
locale/{fr,en}/   # Traductions .po / .mo
Dockerfile, docker-compose.yml, gunicorn.conf.py
package.json, tailwind.config.js   # Pipeline Tailwind CLI (optionnel)
```

## Démarrage rapide (local, SQLite)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env            # DB_ENGINE=sqlite par défaut
python manage.py migrate
python manage.py seed_demo      # contenu de démonstration
python manage.py optimize_images  # génère les versions WebP
python manage.py createsuperuser
python manage.py runserver
```

Ouvrir http://127.0.0.1:8000/ (redirige vers `/fr/`). Admin : `/admin/`.

## Bilingue (FR / EN)

- Langue par défaut : **français**. URLs préfixées : `/fr/...`, `/en/...`.
- Sélecteur de langue dans la navbar (endpoint `set_language`).
- Textes d'interface : balises `{% trans %}` → catalogues `locale/`.
- Contenu éditorial : champs `_fr` / `_en` sur les modèles, résolus selon la
  langue active.

Regénérer / recompiler après modification des templates :

```bash
python manage.py makemessages -l fr -l en --ignore=venv
# éditer locale/en/LC_MESSAGES/django.po
python manage.py compilemessages -l fr -l en
```

## E-mails

Par défaut (dev) : backend **console** (les e-mails s'affichent dans le terminal).
Pour du SMTP réel, renseigner dans `.env` : `EMAIL_HOST`, `EMAIL_PORT`,
`EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `CONTACT_EMAIL`,
`DEFAULT_FROM_EMAIL`.

## Images WebP

`python manage.py optimize_images` convertit les PNG/JPG de `static/media/` en
`.webp`. Les templates utilisent `<picture>` avec `<source type="image/webp">`
et repli sur le format original.

## Build Tailwind CLI (remplacer le CDN Play)

```bash
npm install
npm run build   # -> static/css/tailwind.build.css
```

Puis dans `templates/base.html`, remplacer le `<script src="cdn.tailwindcss.com">`
par `<link rel="stylesheet" href="{% static 'css/tailwind.build.css' %}" />`.

## Production — PostgreSQL & Docker

Avec Docker Compose (PostgreSQL + gunicorn) :

```bash
cp .env.example .env   # DEBUG=False, SECRET_KEY, ALLOWED_HOSTS, DB_ENGINE=postgres
docker compose up --build
# initialiser :
docker compose exec web python manage.py seed_demo
docker compose exec web python manage.py createsuperuser
```

Sans Docker :

- `DEBUG=False`, renseigner `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`.
- `DB_ENGINE=postgres` + variables `DB_*`.
- `python manage.py collectstatic` (WhiteNoise sert les statiques compressés).
- `python manage.py compilemessages`
- Servir via `gunicorn config.wsgi:application -c gunicorn.conf.py`.
```

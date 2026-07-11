from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import (
    Article,
    FAQ,
    JobOffer,
    PartnerLogo,
    Project,
    Service,
    Stat,
    Testimonial,
    TimelineEvent,
)


class Command(BaseCommand):
    help = "Seed the database with bilingual demo content for Togo Rail."

    def handle(self, *args, **options):
        services = [
            {
                "title_fr": "Fret ferroviaire",
                "title_en": "Rail Freight",
                "summary_fr": "Transport de marchandises longue distance, fiable et écologique, à travers le corridor Togo–Sahel.",
                "summary_en": "Reliable, eco-friendly long-haul goods transport across the Togo–Sahel corridor.",
                "icon": "cargo",
                "order": 1,
            },
            {
                "title_fr": "Transport de voyageurs",
                "title_en": "Passenger Transport",
                "summary_fr": "Des liaisons rapides et confortables reliant Lomé aux grandes villes du pays.",
                "summary_en": "Fast, comfortable connections linking Lomé to the country's major cities.",
                "icon": "rail",
                "order": 2,
            },
            {
                "title_fr": "Logistique intégrée",
                "title_en": "Integrated Logistics",
                "summary_fr": "Solutions de bout en bout : entreposage, dernier kilomètre et suivi en temps réel.",
                "summary_en": "End-to-end solutions: warehousing, last-mile delivery and real-time tracking.",
                "icon": "network",
                "order": 3,
            },
            {
                "title_fr": "Ingénierie & infrastructure",
                "title_en": "Engineering & Infrastructure",
                "summary_fr": "Conception, construction et maintenance de voies ferrées de nouvelle génération.",
                "summary_en": "Design, construction and maintenance of next-generation railway lines.",
                "icon": "bolt",
                "order": 4,
            },
            {
                "title_fr": "Sécurité & conformité",
                "title_en": "Safety & Compliance",
                "summary_fr": "Standards internationaux de sécurité et supervision opérationnelle 24/7.",
                "summary_en": "International safety standards and 24/7 operational supervision.",
                "icon": "shield",
                "order": 5,
            },
            {
                "title_fr": "Corridors régionaux",
                "title_en": "Regional Corridors",
                "summary_fr": "Interconnexion avec les réseaux de la CEDEAO pour un commerce ouest-africain fluide.",
                "summary_en": "Interconnection with ECOWAS networks for seamless West-African trade.",
                "icon": "globe",
                "order": 6,
            },
        ]

        stats = [
            {"label_fr": "Kilomètres de voies", "label_en": "Kilometres of track", "value": 1240, "suffix": "+", "order": 1},
            {"label_fr": "Tonnes transportées / an", "label_en": "Tonnes carried / year", "value": 3, "suffix": "M", "order": 2},
            {"label_fr": "Voyageurs par an", "label_en": "Passengers per year", "value": 850, "suffix": "K", "order": 3},
            {"label_fr": "Taux de ponctualité", "label_en": "On-time rate", "value": 98, "suffix": "%", "order": 4},
        ]

        timeline = [
            {"year": "2018", "title_fr": "Vision & fondation", "title_en": "Vision & Founding", "body_fr": "Naissance de Togo Rail avec l'ambition de moderniser la mobilité nationale.", "body_en": "Togo Rail is born with the ambition to modernise national mobility.", "order": 1},
            {"year": "2020", "title_fr": "Premier corridor", "title_en": "First Corridor", "body_fr": "Ouverture de la première ligne de fret entre Lomé et le nord du pays.", "body_en": "Opening of the first freight line between Lomé and the north.", "order": 2},
            {"year": "2023", "title_fr": "Réseau intelligent", "title_en": "Smart Network", "body_fr": "Déploiement du suivi en temps réel et de la supervision numérique.", "body_en": "Rollout of real-time tracking and digital supervision.", "order": 3},
            {"year": "2026", "title_fr": "Expansion régionale", "title_en": "Regional Expansion", "body_fr": "Interconnexion avec les corridors de la CEDEAO.", "body_en": "Interconnection with ECOWAS corridors.", "order": 4},
        ]

        partners = [
            {"name": "CEDEAO", "order": 1},
            {"name": "Port de Lomé", "order": 2},
            {"name": "UEMOA", "order": 3},
            {"name": "AfDB", "order": 4},
            {"name": "Sahel Logistics", "order": 5},
            {"name": "West Africa Trade", "order": 6},
        ]

        body_fr = (
            "Notre approche combine ingénierie de pointe, exploitation intelligente "
            "et respect strict des standards internationaux.\n\n"
            "Chaque projet est piloté par des équipes pluridisciplinaires qui "
            "garantissent qualité, sécurité et durabilité à chaque étape."
        )
        body_en = (
            "Our approach combines cutting-edge engineering, smart operations and "
            "strict adherence to international standards.\n\n"
            "Every project is led by multidisciplinary teams ensuring quality, "
            "safety and sustainability at every step."
        )
        for data in services:
            data.setdefault("body_fr", body_fr)
            data.setdefault("body_en", body_en)
            Service.objects.update_or_create(order=data["order"], defaults=data)
        for data in stats:
            Stat.objects.update_or_create(order=data["order"], defaults=data)
        for data in timeline:
            TimelineEvent.objects.update_or_create(order=data["order"], defaults=data)
        for data in partners:
            PartnerLogo.objects.update_or_create(name=data["name"], defaults=data)

        projects = [
            {"title_fr": "Corridor Lomé–Cinkassé", "title_en": "Lomé–Cinkassé Corridor", "summary_fr": "1 000 km de voie modernisée reliant le port aux frontières du nord.", "summary_en": "1,000 km of upgraded track linking the port to the northern borders.", "year": "2023", "location": "Togo", "order": 1},
            {"title_fr": "Gare intelligente de Lomé", "title_en": "Lomé Smart Station", "summary_fr": "Un hub multimodal de nouvelle génération au cœur de la capitale.", "summary_en": "A next-generation multimodal hub in the heart of the capital.", "year": "2024", "location": "Lomé", "order": 2},
            {"title_fr": "Terminal fret de Kara", "title_en": "Kara Freight Terminal", "summary_fr": "Plateforme logistique automatisée pour le fret régional.", "summary_en": "Automated logistics platform for regional freight.", "year": "2025", "location": "Kara", "order": 3},
        ]
        for data in projects:
            Project.objects.update_or_create(order=data["order"], defaults=data)

        now = timezone.now()
        articles = [
            {"title_fr": "Togo Rail inaugure un nouveau corridor", "title_en": "Togo Rail opens a new corridor", "excerpt_fr": "Une étape majeure pour la connectivité régionale.", "excerpt_en": "A major milestone for regional connectivity.", "body_fr": "Togo Rail poursuit son expansion avec l'ouverture d'un nouveau corridor stratégique.\n\nCe projet renforce le commerce ouest-africain et réduit les délais de transport.", "body_en": "Togo Rail continues its expansion with the opening of a new strategic corridor.\n\nThis project strengthens West-African trade and cuts transport times.", "category_fr": "Infrastructure", "category_en": "Infrastructure", "published_at": now},
            {"title_fr": "La supervision numérique en temps réel", "title_en": "Real-time digital supervision", "excerpt_fr": "Comment la technologie transforme notre réseau.", "excerpt_en": "How technology is transforming our network.", "body_fr": "Grâce à la maintenance prédictive et à la supervision 24/7, notre réseau atteint des niveaux de fiabilité inédits.", "body_en": "Thanks to predictive maintenance and 24/7 supervision, our network reaches unprecedented reliability.", "category_fr": "Innovation", "category_en": "Innovation", "published_at": now},
            {"title_fr": "Une mobilité plus durable", "title_en": "Towards more sustainable mobility", "excerpt_fr": "Le rail au service de la transition écologique.", "excerpt_en": "Rail serving the ecological transition.", "body_fr": "Le transport ferroviaire réduit drastiquement l'empreinte carbone du fret régional.", "body_en": "Rail transport drastically reduces the carbon footprint of regional freight.", "category_fr": "Durabilité", "category_en": "Sustainability", "published_at": now},
        ]
        for data in articles:
            Article.objects.update_or_create(title_en=data["title_en"], defaults=data)

        offers = [
            {"title_fr": "Ingénieur voie ferrée", "title_en": "Track Engineer", "contract_type": "cdi", "description_fr": "Vous concevez et supervisez la construction des voies de nouvelle génération.", "description_en": "You design and supervise the construction of next-generation tracks.", "order": 1},
            {"title_fr": "Responsable exploitation", "title_en": "Operations Manager", "contract_type": "cdi", "description_fr": "Vous pilotez la supervision numérique et la sécurité opérationnelle du réseau.", "description_en": "You lead the digital supervision and operational safety of the network.", "order": 2},
            {"title_fr": "Data analyst logistique", "title_en": "Logistics Data Analyst", "contract_type": "cdd", "description_fr": "Vous optimisez les flux grâce à l'analyse de données en temps réel.", "description_en": "You optimise flows through real-time data analysis.", "order": 3},
        ]
        for data in offers:
            JobOffer.objects.update_or_create(title_en=data["title_en"], defaults=data)

        faqs = [
            {"question_fr": "Quels types de marchandises transportez-vous ?", "question_en": "What kind of goods do you transport?", "answer_fr": "Nous transportons une large gamme de marchandises : conteneurs, vrac, produits agricoles et industriels.", "answer_en": "We carry a wide range of goods: containers, bulk, agricultural and industrial products.", "order": 1},
            {"question_fr": "Comment suivre mon expédition ?", "question_en": "How can I track my shipment?", "answer_fr": "Notre plateforme de suivi en temps réel vous donne une visibilité complète sur vos flux.", "answer_en": "Our real-time tracking platform gives you full visibility over your flows.", "order": 2},
            {"question_fr": "Proposez-vous des solutions sur mesure ?", "question_en": "Do you offer tailored solutions?", "answer_fr": "Oui, nous construisons des solutions logistiques adaptées à chaque besoin.", "answer_en": "Yes, we build logistics solutions tailored to each need.", "order": 3},
            {"question_fr": "Quelle est votre couverture géographique ?", "question_en": "What is your geographic coverage?", "answer_fr": "Nous couvrons le Togo et nous interconnectons aux corridors de la CEDEAO.", "answer_en": "We cover Togo and interconnect with ECOWAS corridors.", "order": 4},
        ]
        for data in faqs:
            FAQ.objects.update_or_create(order=data["order"], defaults=data)

        testimonials = [
            {"author": "Amadou Diallo", "role_fr": "Directeur Logistique, Sahel Trade", "role_en": "Logistics Director, Sahel Trade", "quote_fr": "Togo Rail a transformé notre chaîne d'approvisionnement. Fiabilité et ponctualité exemplaires.", "quote_en": "Togo Rail transformed our supply chain. Exemplary reliability and punctuality.", "order": 1},
            {"author": "Fatou Mensah", "role_fr": "CEO, West Africa Cargo", "role_en": "CEO, West Africa Cargo", "quote_fr": "Un partenaire stratégique de confiance pour notre expansion régionale.", "quote_en": "A trusted strategic partner for our regional expansion.", "order": 2},
            {"author": "Kwame Osei", "role_fr": "Ministre des Transports (invité)", "role_en": "Transport Minister (guest)", "quote_fr": "Une infrastructure qui incarne l'avenir de la mobilité africaine.", "quote_en": "Infrastructure that embodies the future of African mobility.", "order": 3},
        ]
        for data in testimonials:
            Testimonial.objects.update_or_create(author=data["author"], defaults=data)

        self.stdout.write(self.style.SUCCESS("Demo content seeded successfully."))

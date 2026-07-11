from django.core.management.base import BaseCommand

from core.models import PartnerLogo, Service, Stat, TimelineEvent


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

        for data in services:
            Service.objects.update_or_create(order=data["order"], defaults=data)
        for data in stats:
            Stat.objects.update_or_create(order=data["order"], defaults=data)
        for data in timeline:
            TimelineEvent.objects.update_or_create(order=data["order"], defaults=data)
        for data in partners:
            PartnerLogo.objects.update_or_create(name=data["name"], defaults=data)

        self.stdout.write(self.style.SUCCESS("Demo content seeded successfully."))

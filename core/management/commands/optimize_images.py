from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None


class Command(BaseCommand):
    help = "Generate optimized WebP versions of PNG/JPG images in static/media."

    def add_arguments(self, parser):
        parser.add_argument("--quality", type=int, default=82)

    def handle(self, *args, **options):
        if Image is None:
            self.stderr.write("Pillow is required. Run: pip install Pillow")
            return

        quality = options["quality"]
        media_dir = Path(settings.BASE_DIR) / "static" / "media"
        if not media_dir.exists():
            self.stderr.write(f"No such directory: {media_dir}")
            return

        count = 0
        for ext in ("*.png", "*.jpg", "*.jpeg"):
            for src in media_dir.glob(ext):
                dest = src.with_suffix(".webp")
                if dest.exists() and dest.stat().st_mtime >= src.stat().st_mtime:
                    continue
                try:
                    with Image.open(src) as im:
                        if im.mode in ("P", "LA"):
                            im = im.convert("RGBA")
                        im.save(dest, "WEBP", quality=quality, method=6)
                    count += 1
                    self.stdout.write(f"  ✓ {src.name} → {dest.name}")
                except Exception as exc:  # pragma: no cover
                    self.stderr.write(f"  ✗ {src.name}: {exc}")

        self.stdout.write(self.style.SUCCESS(f"Done. {count} image(s) converted."))

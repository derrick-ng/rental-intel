from django.core.management.base import BaseCommand
from listings.models import Listing
from listings.detail_scraper import scrape_listing_details
import time, random
from listings.utils import mark_inactive_in_production

class Command(BaseCommand):
    def handle(self, *args, **options):
        listings = Listing.objects.filter(active=True)

        total = listings.count()
        self.stdout.write(f"Checking {total} active listings")

        new_inactive = 0
        changed = 0
        unchanged = 0

        inactive_ids = []

        for index, listing in enumerate(listings, 1):
            try:
                self.stdout.write(f"[{index}/{total}] Checking: {listing.url}")

                details = scrape_listing_details(listing.url)

                if not details or all(v is None or v is False for v in details.values()):
                    self.stdout.write(
                        self.style.WARNING(f"Listing appears removed, marking inactive")
                    )

                    listing.active = False
                    listing.save()
                    new_inactive += 1
                    inactive_ids.append(listing.craigslist_id)
                    time.sleep(random.uniform(1.5, 3))
                    continue
            
                unchanged += 1

                time.sleep(random.uniform(1.5, 3))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error checking: {e}"))
    
        self.stdout.write(
            self.style.SUCCESS(
                f"\n=== Update Complete ===\n"
                f"Unchanged: {unchanged}\n"
                f"Changed: {changed}\n"
                f"New inactive: {new_inactive}\n"
                f"Total checked: {total}"
            )
        )

        mark_inactive_in_production(inactive_ids)
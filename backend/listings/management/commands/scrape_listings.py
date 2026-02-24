from django.core.management.base import BaseCommand
from listings.models import Listing
from listings.scraper import scrape_list_urls
from listings.etl import clean_listings_data
from listings.geocoding import geocode_address
from listings.score_listing import score_best_value, score_below_market, score_price_per_sqft
from listings.analytics import get_neighborhood_stats
from listings.utils import sync_new_listings_to_production
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        listings_data = scrape_list_urls()
        cleaned_data = clean_listings_data(listings_data)

        stats = get_neighborhood_stats()
        neighborhood_avgs = {stat['location']: stat['avg_price'] for stat in stats}

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for data in cleaned_data:
            duplicate_exists = Listing.objects.filter(
                title=data['title'],
                location=data['location'],
                price=data['price']
            ).exclude(craigslist_id=data['craigslist_id']).exists()

            if duplicate_exists:
                skipped_count += 1
                continue

            data['best_value'] = score_best_value(data, neighborhood_avgs)
            data['below_market'] = score_below_market(data, neighborhood_avgs)
            data['price_per_sqft'] = score_price_per_sqft(data)

            listing, created = Listing.objects.get_or_create(
                craigslist_id=data['craigslist_id'],
                defaults=data
            )
            
            if created:
                created_count += 1

                if listing.address and not listing.latitude:
                    coords = geocode_address(listing.address)

                    if coords:
                        listing.latitude = coords['lat']
                        listing.longitude = coords['lon']
                        listing.save()
                    time.sleep(.2)
            else:
                for key, value in data.items():
                    setattr(listing, key, value)

                listing.save()
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Created: {created_count}, Updated: {updated_count}"
            )
        )
    
        sync_new_listings_to_production()
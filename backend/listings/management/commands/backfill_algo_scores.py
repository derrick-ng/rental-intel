from django.core.management.base import BaseCommand
from listings.models import Listing
from listings.score_listing import score_below_market, score_best_value, score_price_per_sqft
from listings.analytics import get_neighborhood_stats

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("backfill algo score start")
        listings_to_update = []
        neighborhood_stats = get_neighborhood_stats()
        neighborhood_avgs = {neighborhood['location']: neighborhood['avg_price'] for neighborhood in neighborhood_stats}

        listings = Listing.objects.filter(
            active=True,
            sqft__gt=0,
            price__isnull=False,
            price__gt=0,
            bedrooms__isnull=False,
        )

        print('-----starting scoring functions here-----')
        for listing in listings:
            listing.below_market = score_below_market(listing, neighborhood_avgs)
            listing.best_value = score_best_value(listing, neighborhood_avgs)
            listing.price_per_sqft = score_price_per_sqft(listing)
            
            listings_to_update.append(listing)

        Listing.objects.bulk_update(listings_to_update, ['below_market', 'best_value', 'price_per_sqft'])
        print('------scoring finished------')
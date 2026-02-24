from django.core.management.base import BaseCommand
from listings.utils import find_inactive_listings, mark_inactive_in_development, mark_inactive_in_production
    
class Command(BaseCommand):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
    }

    def handle(self, *args, **options):
        self.clean_below_market_deals()
        self.clean_best_value_deals()
        self.clean_best_price_per_sqft_deals()

    def clean_below_market_deals(self):
        print("Below Market deal cleaner start")

        inactive_ids = find_inactive_listings(order_by='-below_market')

        mark_inactive_in_development(inactive_ids)
        mark_inactive_in_production(inactive_ids)

        print('Below Market deals data refreshed\n')

    def clean_best_value_deals(self):
        print("Best value deal cleaner start")
        inactive_ids = find_inactive_listings(order_by='-best_value')
        
        mark_inactive_in_development(inactive_ids)
        mark_inactive_in_production(inactive_ids)

        print('Best value deals data refreshed\n')

    def clean_best_price_per_sqft_deals(self):
        print("Best price per sqft cleaner start")
        inactive_ids = find_inactive_listings(order_by='price_per_sqft')

        mark_inactive_in_development(inactive_ids)
        mark_inactive_in_production(inactive_ids)

        print('Best price per sqft data refreshed\n')
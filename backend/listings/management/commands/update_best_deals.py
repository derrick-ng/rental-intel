from django.core.management.base import BaseCommand
from listings.models import Listing
from listings.utils import find_inactive_listings, mark_inactive_in_development, mark_inactive_in_production
from bs4 import BeautifulSoup
import requests, time, random

# base command - makes sure each best deals section has 10 fresh listings
# add to celery to run once a day, after daily scraper

# Implementation:
# go through each best deal category individually
    # query for each section - find all listings (active), sort in descending order (best first)
# check each listing for inactivity
    # get request to listing.url
    # if inactive: store listing.id
    # if active: do nothing, increment counter
        # counter to keep track until 10 listings are found
# bulk update all inactive listings to inactive
    
class Command(BaseCommand):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
    }

    def handle(self, *args, **options):
        self.clean_below_market_deals()

    def clean_below_market_deals(self):
        inactive_ids = find_inactive_listings(order_by='-below_market')

        mark_inactive_in_development(inactive_ids)
        mark_inactive_in_production(inactive_ids)

        print('Below Market deals data refreshed')

    def clean_best_value_deals(self):
        pass

    def clean_best_price_per_sqft_deals(self):
        pass
from django.core.management.base import BaseCommand
from listings.models import Listing
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
        listings = Listing.objects.filter(
            active=True,
        ).order_by('-below_market')

        active_listings = 0
        inactive_listings = []

        for listing in listings:
            if active_listings >= 10:
                break
            
            time.sleep(random.uniform(3, 5))

            print(f'[{active_listings}/10] Checking: {listing.url}')

            try:
                response = requests.get(listing.url, headers=self.headers, timeout=10)
                response.raise_for_status()
            except Exception as e:
                print(f"Error fetching {listing.url}: {e}")
                continue
            
            soup = BeautifulSoup(response.content, 'lxml')
            removed = soup.find('div', id='has_been_removed')

            if removed:
                print(f'Listing has been flagged/removed')
                inactive_listings.append(listing.id)
                continue
            
            print('Listing is active')
            active_listings += 1
        
        Listing.objects.filter(
            id__in=inactive_listings
        ).update(active=False)

        print('Below Market deals data refreshed')

    def clean_best_value_deals(self):
        pass

    def clean_best_price_per_sqft_deals(self):
        pass
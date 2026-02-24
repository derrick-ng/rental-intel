from listings.models import Listing
from listings.serializers import ListingSerializer
from bs4 import BeautifulSoup
import os, requests, time, random

def find_inactive_listings(order_by=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
    }

    listings = Listing.objects.filter(
        active=True
    )

    if order_by:
        listings = listings.order_by(order_by)

    active_listings = 0
    inactive_ids = []

    for listing in listings:
        if active_listings >= 10:
            break

        time.sleep(random.uniform(3, 5))

        print(f'[{active_listings} active] Checking: {listing.url}')

        try:
            response = requests.get(listing.url, headers=headers, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print(f'Error fetching inactive listing: {e}')
            continue

        soup = BeautifulSoup(response.content, 'lxml')
        removed = soup.find('div', id='has_been_removed')

        if removed:
            print(f'Listing has been flagged/removed')
            inactive_ids.append(listing.craigslist_id)
            continue
        
        print('Listing is active')
        active_listings += 1
    
    return inactive_ids

def mark_inactive_in_development(inactive_ids):
    if not inactive_ids:
        print('No listings marked as inactive')
        return
    
    updated = Listing.objects.filter(
        craigslist_id__in=inactive_ids
    ).update(active=False)

    print(f"DEVELOPMENT: Marked {updated} listings as inactive")

def mark_inactive_in_production(inactive_ids):
    if not inactive_ids:
        print('No listings marked as inactive')
        return

    PROD_URL = os.getenv('PRODUCTION_API_URL')

    try:
        print(f'Marking {len(inactive_ids)} listings as inactive in production')

        response = requests.post(
            f'{PROD_URL}/api/listings/mark_inactive/',
            json={'craigslist_ids': inactive_ids}
        )

        status_code = response.status_code
        if status_code == 200:
            result = response.json()
            print(f"PRODUCTION: Marked {result['marked_inactive']} as inactive")
        else:
            print(f'Production inactive async failed: {status_code}')

    except Exception as e:
        print(f'Production inactive sync error: {e}')
        

def sync_new_listings_to_production():
    PROD_URL = os.getenv('PRODUCTION_API_URL')

    try:
        listings = Listing.objects.filter(
            active=True
        )
        serializer = ListingSerializer(listings, many=True)
        data = serializer.data

        print(f'Syncing {len(data)} listings to production')

        response = requests.post(
            f'{PROD_URL}/api/listings/bulk_create_listings/',
            json=data
        )

        status_code = response.status_code
        if status_code == 200:
            result = response.json()
            print(f"PRODUCTION: Created: {result['created']}")
            print(f"PRODUCTION: Updated: {result['updated']}")
        else:
            print(f'Production new listing sync failed: {status_code}')

    except Exception as e:
        print(f'Production new listing sync error: {e}')

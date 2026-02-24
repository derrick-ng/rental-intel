import os, requests

def mark_inactive_in_production(inactive_ids):
    if not inactive_ids:
        print('No listings marked as inactive')
        return

    prod_url = os.getenv('PRODUCTION_API_URL')

    try:
        print(f'Marking {len(inactive_ids)} listings as inactive in production')

        response = requests.post(
            f'{prod_url}/api/listings/mark_inactive/',
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
    pass
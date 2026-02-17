from .models import Listing
from .analytics import get_neighborhood_stats

def get_overall_best_value():
    stats = get_neighborhood_stats()
    neighborhood_avgs = {stat['location']: stat['avg_price'] for stat in stats}

    listings = Listing.objects.filter(
        active=True,
    ).order_by('-best_value')[:10]

    scored_listings = []

    for listing in listings:
        price = listing.price
        bedrooms = listing.bedrooms
        location = listing.location
        
        # calculate studios as 1 bedroom
        effective_bedrooms = bedrooms or 1
        price_per_bedroom = round(price / effective_bedrooms)

        details = {
            'price_per_sqft': listing.price_per_sqft,
            'price_per_bedroom': price_per_bedroom
        }

        avg_price = neighborhood_avgs.get(location)
        if avg_price:
            percent_below_avg = round((avg_price - price) / avg_price * 100, 1)

            details['percent_below_avg'] = percent_below_avg

        scored_listings.append({
            'id': listing.id,
            'title': listing.title,
            'price': price,
            'bedrooms': bedrooms,
            'bathrooms': float(listing.bathrooms) if listing.bathrooms else None,
            'sqft': listing.sqft,
            'location': location,
            'parking': listing.parking,
            'laundry_type': listing.laundry_type,
            'url': listing.url,
            'total_score': round(listing.best_value, 1),
            'details': details
        })

    return scored_listings


def get_good_deals():
    stats = get_neighborhood_stats()
    neighborhood_avgs = {stat['location']: stat['avg_price'] for stat in stats}

    listings = Listing.objects.filter(
        active=True,
    ).order_by('-below_market')[:10]

    good_deals = []

    for listing in listings:
        location = listing.location
        price = listing.price

        avg_price = neighborhood_avgs.get(location)
        if not avg_price:
            continue

        savings = avg_price - price

        good_deals.append({
            'id': listing.id,                
            'title': listing.title,
            'price': price,
            'location': location,
            'avg_price': round(avg_price, 2),
            'savings': round(savings, 2),
            'percent_below_avg': round((avg_price - price) / avg_price * 100, 1),
            'url': listing.url,
        })
    
    return good_deals

def get_best_price_per_sqft():
    listings = Listing.objects.filter(
        active=True,
        bedrooms__isnull=False,
        sqft__isnull=False,
        sqft__gt=0,
    )

    best_deals = []

    for listing in listings:
        price_per_sqft = listing.price / listing.sqft

        if price_per_sqft < 1.50 or price_per_sqft > 6.00:
            continue
            
        best_deals.append({
            'id': listing.id,
            'title': listing.title,
            'price': listing.price,
            'sqft': listing.sqft,
            'price_per_sqft': round(price_per_sqft, 2),
            'bedrooms': listing.bedrooms,
            'bathrooms': float(listing.bathrooms) if listing.bathrooms else None,
            'location': listing.location,
            'url': listing.url,
        })

    best_deals.sort(key=lambda x: x['price_per_sqft'])

    return best_deals[:10]

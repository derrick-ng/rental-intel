from django.db.models import Avg, Count, Min, Max
from .models import Listing

def get_neighborhood_stats():
    stats = Listing.objects.filter(
        active=True,
        bedrooms__isnull=False,
        price__gte=1000,
        price__lte=6000,
        data_quality__gte=50,
    ).values('location').annotate(
        avg_price=Avg('price'),
        median_bedrooms=Avg('bedrooms'),
        listing_count=Count('id'),
        min_price=Min('price'),
        max_price=Max('price'),
        avg_sqft=Avg('sqft')
    ).order_by('-listing_count')

    return list(stats)

def get_price_distribution():
    buckets = [
        (1, 1500),
        (1500, 2000),
        (2000, 2500),
        (2500, 3000),
        (3500, 4000),
        (4000, 5000),
        (5000, 10000),
    ]
    
    distribution = []
    for min_price, max_price in buckets:
        count = Listing.objects.filter(
            active=True,
            price__gte=min_price,
            price__lt=max_price
        ).count()

        distribution.append({
            'range': f'${min_price}-${max_price}',
            'count': count
        })
    return distribution

def get_overall_stats():
    listings = Listing.objects.filter(
        active=True,
    )

    stats = {
        'total_listings': listings.count(),
        'avg_price': round(listings.aggregate(Avg('price'))['price__avg'] or 0, 2),
        'median_bedrooms': round(listings.aggregate(Avg('bedrooms'))['bedrooms__avg'] or 0, 1),
        'locations_count': listings.values('location').distinct().count(),
        'with_details': listings.filter(
            bedrooms__isnull=False,
            bathrooms__isnull=False,
            address__isnull=False,
            sqft__isnull=False,
            laundry_type__isnull=False,
            parking__isnull=False,
        ).count(),
    }

    return stats
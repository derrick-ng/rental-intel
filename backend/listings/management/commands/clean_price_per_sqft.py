from django.core.management.base import BaseCommand
from listings.models import Listing

class Command(BaseCommand):
    def handle(self, *args, **options):
        Listing.objects.filter(price_per_sqft__gte=100).update(price_per_sqft=0)


from django.db import models
from django.utils import timezone

#only for craigslist for now
class Listing(models.Model):

    #essential data
    craigslist_id = models.CharField(max_length=255, unique=True)
    url = models.URLField()
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    location = models.CharField(max_length=255)

    #extra details
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    sqft = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    #amenities
    cats_allowed = models.BooleanField(null=True, default=False)
    dogs_allowed = models.BooleanField(null=True, default=False)
    laundry_type = models.CharField(
        max_length=50,
        choices=[
            ('none', 'No Laundry'),
            ('in_unit', 'In-Unit'),
            ('on_site', 'On-Site/In Building'),
        ],

        null=True,
        blank=True,
    )
    parking = models.CharField(
        max_length=50,
        choices=[
            ('none', 'No Parking'),
            ('street', 'Street Parking'),
            ('off_street', 'Off-Street Parking'),
            ('garage', 'Garage'),
            ('carport', 'Carport'),
        ],
        null=True,
        blank=True
    )
    
    #extra misc amenities
    extra_amenities = models.TextField(null=True, blank=True)

    #extra analysis data
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    #metadata
    scraped_at = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    data_quality = models.IntegerField(default=0)
    
    #best deal scores
    best_value = models.IntegerField(default=0)
    below_market = models.IntegerField(default=0)
    price_per_sqft = models.DecimalField(default=0, max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.title} - {self.price}"
    
    class Meta:
        ordering = ['-scraped_at']
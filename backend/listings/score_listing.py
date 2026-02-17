def score_best_value(listing_data, neighborhood_avgs):
    """
    ai weights
    - Price per sqft (30%)
    - Below neighborhood average (25%)
    - Price per bedroom (20%)
    - Amenities (parking, laundry) (15%)
    - Data quality (10%)
    """

    if listing_data.get('bedrooms') is None or listing_data.get('sqft') is None or listing_data.get('sqft', 0) <= 0:
        return 0

    price = listing_data['price']
    sqft = listing_data['sqft']
    location = listing_data['location']
    bedrooms = listing_data['bedrooms']
    parking = listing_data['parking']
    laundry_type = listing_data['laundry_type']
    cats_allowed = listing_data['cats_allowed']
    dogs_allowed = listing_data['dogs_allowed']
    data_quality = listing_data['data_quality']

    score = 0

    #Factor 1: Price Per Sqft
    price_per_sqft = price / sqft
    
    if 1.50 <= price_per_sqft <= 6.00:
        if price_per_sqft <= 2.50:
            sqft_score = 30
        elif price_per_sqft <= 3.00:
            sqft_score = 25
        elif price_per_sqft <= 3.50:
            sqft_score = 20
        elif price_per_sqft <= 4.00:
            sqft_score = 15
        else:
            sqft_score = 10
    else:
        #unreasonable price per sqft, do not score
        return 0
        
    score += sqft_score

    #Factor 2: Below Neighborhood Average
    avg_price = neighborhood_avgs.get(location)

    if avg_price is not None:
        percent_of_avg = (price / avg_price) * 100
        
        if percent_of_avg <= 70:
            market_score = 25
        elif percent_of_avg <= 80:
            market_score = 20
        elif percent_of_avg <= 90:
            market_score = 15
        elif percent_of_avg <= 100:
            market_score = 10
        else:
            market_score = 5

        score += market_score

    #Factor 3: Price Per Bedroom
    #edge case for studio apartments
    effective_bedrooms = bedrooms or 1

    price_per_br = price / effective_bedrooms

    if price_per_br <= 1500:
        score += 20
    elif price_per_br <= 2000:
        score += 15
    elif price_per_br <= 2500:
        score += 10
    elif price_per_br <= 3000:
        score += 5

    amenity_score = 0
    
    #Factor 4: Amenities (Laundry & Pets)
    if parking == 'garage':
        amenity_score += 7
    elif parking == 'off_street':
        amenity_score += 5
    elif parking == 'carport':
        amenity_score += 3
    elif parking == 'street':
        amenity_score += 1
    
    # Laundry
    if laundry_type == 'in_unit':
        amenity_score += 5
    elif laundry_type == 'on_site':
        amenity_score += 3
    
    # Pets
    if cats_allowed and dogs_allowed:
        amenity_score += 3
    elif cats_allowed or dogs_allowed:
        amenity_score += 2
    
    score += amenity_score
    
    # Factor 5: Data quality
    quality_score = (data_quality / 100) * 10
    score += quality_score
    
    return round(score)

def score_below_market(listing_data, neighborhood_avgs):
    location = listing_data['location']
    price = listing_data['price']

    avg_price = neighborhood_avgs.get(location)

    if avg_price is None:
        return 0
    
    # minimum 10% saving to score
    if price >= avg_price * .9:
        return 0
    
    percentage_below = ((avg_price - price) / avg_price ) * 100

    return round(percentage_below, 1)

def score_price_per_sqft(listing_data):
    price = listing_data['price']
    sqft = listing_data['sqft']

    if not sqft or sqft <= 0:
        return 0

    price_per_sqft = price / sqft

    if price_per_sqft < 1.50 or price_per_sqft > 6.00:
        return 0

    return round(price_per_sqft, 2)
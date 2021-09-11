def is_valid_region(region):
    """ Checks if region is valid
    """
    regionToCheck = region.upper()
    valid_regions = [
        "BR1",
        "EUN1",
        "EUW1",
        "JP1",
        "KR",
        "LA1",
        "LA2",
        "NA1",
        "OC1",
        "TR1",
        "RU"
    ]
    if regionToCheck in valid_regions:
        return True
    else:
        return False


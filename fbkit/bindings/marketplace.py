from .. import proxies

BINDINGS = {
    'createListing': [
        ('listing_id', int, {}),
        ('show_on_profile', bool, {}),
        ('listing_attrs', str, {}),
    ],
    'getCategories': [],
    'getListings': [
        ('listing_ids', list, {}),
        ('uids', list, {}),
    ],
    'getSubCategories': [
        ('category', str, {}),
    ],
    'removeListing': [
        ('listing_id', int, {}),
        ('status', str, {}),
    ],
    'search': [
        ('category', str, {'optional': True}),
        ('subcategory', str, {'optional': True}),
        ('query', str, {'optional': True}),
    ],
}

Proxy = proxies.build_proxy('marketplace', BINDINGS)

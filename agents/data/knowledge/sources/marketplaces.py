"""
==========================================================
AI Publishing OS V7
Knowledge Source
Marketplaces
==========================================================
"""

MARKETPLACES = [
    {
        "id": "amazon",
        "name": "Amazon KDP",
        "currency": "USD",
        "country": "Global",
        "active": True,
    },
    {
        "id": "etsy",
        "name": "Etsy",
        "currency": "USD",
        "country": "Global",
        "active": True,
    },
    {
        "id": "gumroad",
        "name": "Gumroad",
        "currency": "USD",
        "country": "Global",
        "active": True,
    },
]


def get_all():
    """Return all supported marketplaces."""
    return MARKETPLACES


def get(marketplace_id: str):
    """Return a marketplace by id."""

    marketplace_id = marketplace_id.lower()

    for marketplace in MARKETPLACES:
        if marketplace["id"] == marketplace_id:
            return marketplace

    return None


def exists(marketplace_id: str):
    """Check if marketplace exists."""

    return get(marketplace_id) is not None
"""
AI Publishing OS V7
Marketplace Source
"""

MARKETPLACES = [
    {
        "id": "amazon",
        "name": "Amazon KDP",
        "currency": "USD",
    },
    {
        "id": "etsy",
        "name": "Etsy",
        "currency": "USD",
    },
    {
        "id": "gumroad",
        "name": "Gumroad",
        "currency": "USD",
    },
]


def get_all():
    return MARKETPLACES


def get(marketplace_id):
    return next((m for m in MARKETPLACES if m["id"] == marketplace_id), None)
from collections.abc import Callable

from app.models import Product

_SORT_KEYS: dict[str, Callable[[Product], object]] = {
    "name": lambda p: p.name,
    "price": lambda p: p.price,
}

PRODUCTS = [
    Product(id=1, name="Zenbook 14 OLED", category="Laptop", price=42900),
    Product(id=2, name="ROG Zephyrus G14", category="Gaming Laptop", price=62900),
    Product(id=3, name="ProArt P16", category="Creator Laptop", price=79900),
    Product(id=4, name="TUF Gaming A15", category="Gaming Laptop", price=38900),
    Product(id=5, name="ROG Ally X", category="Handheld", price=26900),
    Product(id=6, name="ProArt Display PA279CRV", category="Monitor", price=15900),
]


def list_products(
    *,
    q: str | None = None,
    sort: str | None = None,
    order: str = "asc",
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[Product], int]:
    results = PRODUCTS.copy()

    if q is not None:
        q_lower = q.lower()
        results = [
            p
            for p in results
            if q_lower in p.name.lower() or q_lower in p.category.lower()
        ]

    if sort is not None:
        key_fn = _SORT_KEYS.get(sort)
        if key_fn is None:
            raise ValueError(f"Invalid sort field: {sort!r}")
        reverse = order == "desc"
        results = sorted(results, key=key_fn, reverse=reverse)

    total = len(results)
    start = (page - 1) * page_size
    results = results[start : start + page_size]

    return results, total


def get_product(product_id: int) -> Product | None:
    return next((product for product in PRODUCTS if product.id == product_id), None)


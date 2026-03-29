import os
from decimal import Decimal

import django
from django.conf import settings
from django.utils.text import slugify


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skinaura.settings")
django.setup()

from home.models import Product  # noqa: E402


PRODUCTS_BY_CATEGORY = {
    "Moisturizer": [
        "Pond's Light Moisturizer",
        "Nivea Soft Cream",
        "Cetaphil Moisturizing Cream",
        "Lakme Peach Milk Moisturizer",
        "Himalaya Nourishing Skin Cream",
        "Mamaearth Oil-Free Moisturizer",
        "WOW Aloe Vera Gel Moisturizer",
        "Plum Green Tea Moisturizer",
        "Neutrogena Hydro Boost Gel",
        "Minimalist Sepicalm Moisturizer",
    ],
    "Sunscreen": [
        "Lakme Sun Expert SPF 50",
        "Neutrogena Ultra Sheer Sunscreen",
        "Lotus Herbals Safe Sun SPF 40",
        "Mamaearth Sunscreen SPF 50",
        "WOW Sunscreen Matte Finish",
        "Minimalist SPF 50 Sunscreen",
        "Biotique Bio Sandalwood Sunscreen",
        "Nivea Sun Protect SPF 30",
        "Pond's Sun Protect Cream",
        "Garnier UV Bright Sunscreen",
    ],
    "Serum": [
        "Mamaearth Vitamin C Serum",
        "Minimalist Niacinamide Serum",
        "WOW Vitamin C Serum",
        "Plum Vitamin C Serum",
        "Garnier Bright Complete Serum",
        "Lakme Absolute Argan Oil Serum",
        "Biotique Vitamin C Serum",
        "L'Oreal Revitalift Serum",
        "Pond's Bright Beauty Serum",
        "Neutrogena Rapid Wrinkle Repair Serum",
    ],
    "Toner": [
        "Biotique Cucumber Toner",
        "Plum Green Tea Toner",
        "Mamaearth Rose Water Toner",
        "WOW Skin Science Toner",
        "Himalaya Refreshing Toner",
        "Garnier Skin Naturals Toner",
        "Minimalist PHA Toner",
        "Khadi Natural Rose Water",
        "Neutrogena Alcohol-Free Toner",
        "Lotus Herbals Basiltone Toner",
    ],
    "Face Mask / Scrub": [
        "Himalaya Neem Face Pack",
        "Mamaearth Ubtan Face Mask",
        "WOW Charcoal Face Mask",
        "Biotique Fruit Face Pack",
        "Garnier Bright Complete Mask",
        "Lotus Herbals Clay Mask",
        "Pond's Mineral Clay Mask",
        "Nivea Rice Scrub",
        "Clean & Clear Blackhead Scrub",
        "St. Ives Apricot Scrub",
    ],
    "Face Wash / Cleanser": [
        "Cetaphil Gentle Cleanser",
        "Himalaya Neem Face Wash",
        "Nivea Face Wash",
        "Clean & Clear Foaming Face Wash",
        "Garnier Bright Complete Face Wash",
        "Pond's Pure Detox Face Wash",
        "Mamaearth Tea Tree Face Wash",
        "Biotique Bio Honey Gel Cleanser",
        "WOW Vitamin C Face Wash",
        "Minimalist Salicylic Acid Cleanser",
    ],
}

PRICE_BY_CATEGORY = {
    "Moisturizer": 299,
    "Sunscreen": 399,
    "Serum": 549,
    "Toner": 279,
    "Face Mask / Scrub": 349,
    "Face Wash / Cleanser": 249,
}

CATEGORY_COLOR = {
    "Moisturizer": "#7DCFB6",
    "Sunscreen": "#F4D35E",
    "Serum": "#EE964B",
    "Toner": "#9BC1BC",
    "Face Mask / Scrub": "#C2AFF0",
    "Face Wash / Cleanser": "#84A59D",
}


def make_svg(product_name: str, category: str) -> str:
    color = CATEGORY_COLOR.get(category, "#BDBDBD")
    escaped_name = (
        product_name.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return f"""<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"1200\" height=\"1200\" viewBox=\"0 0 1200 1200\">\n  <rect width=\"1200\" height=\"1200\" fill=\"{color}\"/>\n  <rect x=\"80\" y=\"80\" width=\"1040\" height=\"1040\" fill=\"white\" rx=\"40\" ry=\"40\"/>\n  <text x=\"600\" y=\"520\" text-anchor=\"middle\" font-size=\"56\" font-family=\"Arial, sans-serif\" fill=\"#222\">SkinAura</text>\n  <text x=\"600\" y=\"610\" text-anchor=\"middle\" font-size=\"44\" font-family=\"Arial, sans-serif\" fill=\"#333\">{escaped_name}</text>\n  <text x=\"600\" y=\"700\" text-anchor=\"middle\" font-size=\"34\" font-family=\"Arial, sans-serif\" fill=\"#555\">{category}</text>\n</svg>\n"""


def seed_products() -> None:
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    products_dir = os.path.join(settings.MEDIA_ROOT, "products")
    os.makedirs(products_dir, exist_ok=True)

    created = 0
    updated = 0

    for category, names in PRODUCTS_BY_CATEGORY.items():
        for name in names:
            filename = f"{slugify(name)}.svg"
            abs_path = os.path.join(products_dir, filename)
            rel_path = f"products/{filename}"

            with open(abs_path, "w", encoding="utf-8") as image_file:
                image_file.write(make_svg(name, category))

            description = (
                f"{name} is a {category.lower()} product suitable for daily skincare."
            )
            defaults = {
                "price": PRICE_BY_CATEGORY.get(category, 299),
                "description": description,
                "stock": 100,
                "image": rel_path,
            }
            product, was_created = Product.objects.update_or_create(
                name=name,
                defaults=defaults,
            )

            if was_created:
                created += 1
            else:
                updated += 1

            if product.image.name != rel_path:
                product.image = rel_path
                product.save(update_fields=["image"])

    total = Product.objects.count()
    print(f"Seed complete. Created: {created}, Updated: {updated}, Total products: {total}")


if __name__ == "__main__":
    seed_products()
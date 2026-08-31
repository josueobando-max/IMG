# Stock SEO Image Library - for AI agents

389 royalty-free stock images across 23 home & auto service trades,
sized 1536x1024 WebP. Intended for building flyers, ads and social graphics.

## How to use this library

1. Fetch the machine-readable index: **`https://josueobando-max.github.io/IMG/manifest.json`**
2. Filter `images[]` by `category` (or `category_slug`) and read `title` to pick a fitting shot.
3. Download the image directly from its `file` path (or the `url` field when present).
   Every image is a direct, public, hot-linkable URL - no auth, no redirect.
4. A flat newline-separated list of every image URL is at **`https://josueobando-max.github.io/IMG/urls.txt`**.
   A spreadsheet-friendly index is at **`https://josueobando-max.github.io/IMG/manifest.csv`**.

### manifest.json image record

```json
{
  "category": "Auto Detailing",
  "category_slug": "auto-detailing",
  "title": "Ceramic coating maintenance products used to keep a car finish clean and glossy",
  "id": "auto-detailing/ceramic-coating-maintenance-products-used-to-keep-a-car-finish-clean-and-glossy",
  "file": "images/auto-detailing/ceramic-coating-maintenance-products-used-to-keep-a-car-finish-clean-and-glossy.webp",
  "thumb": "thumbs/auto-detailing/ceramic-coating-maintenance-products-used-to-keep-a-car-finish-clean-and-glossy.webp",
  "original": "ceramic_coating_maintenance_products_used_to_keep_a_car_finish_clean_and_glossy.png",
  "width": 1536,
  "height": 1024,
  "bytes": 177812,
  "url": "https://josueobando-max.github.io/IMG/images/auto-detailing/ceramic-coating-maintenance-products-used-to-keep-a-car-finish-clean-and-glossy.webp",
  "thumb_url": "https://josueobando-max.github.io/IMG/thumbs/auto-detailing/ceramic-coating-maintenance-products-used-to-keep-a-car-finish-clean-and-glossy.webp"
}
```

## Categories

| Category | Slug | Images |
|---|---|---|
| Auto Detailing | `auto-detailing` | 4 |
| Auto Repair & Maintenance | `auto-repair-and-maintenance` | 5 |
| Car Audio & Electronics | `car-audio-and-electronics` | 7 |
| Cleaning | `cleaning` | 28 |
| Commercial Doors | `commercial-doors` | 5 |
| Concrete & Floor Coatings | `concrete-and-floor-coatings` | 9 |
| Fencing & Decks | `fencing-and-decks` | 20 |
| Flooring | `flooring` | 21 |
| General Contracting & Remodeling | `general-contracting-and-remodeling` | 5 |
| HVAC | `hvac` | 6 |
| Handyman & Installations | `handyman-and-installations` | 3 |
| Junk Removal | `junk-removal` | 8 |
| Kitchen & Bath Remodeling | `kitchen-and-bath-remodeling` | 10 |
| Landscaping & Hardscaping | `landscaping-and-hardscaping` | 42 |
| Masonry & Exterior | `masonry-and-exterior` | 9 |
| Moving | `moving` | 4 |
| Painting & Exterior | `painting-and-exterior` | 24 |
| Plumbing | `plumbing` | 15 |
| Pool Services | `pool-services` | 12 |
| Roofing & Gutters | `roofing-and-gutters` | 63 |
| Shipping Services (Envios) | `shipping-services-envios` | 4 |
| Tree Services | `tree-services` | 81 |
| Window Treatments | `window-treatments` | 4 |

## Notes for flyer production

- All images are 3:2 landscape (1536x1024). Crop to 4:5 or 9:16 from the centre-weighted
  subject; most shots keep the subject centred with usable negative space on one side.
- Filenames are descriptive of the scene - use `title` as the caption/alt hint.
- `*-variant-1..4` files are alternative takes of the same concept; pick one per layout so a
  multi-panel flyer does not repeat a near-identical frame.
- No text or logos are burned into these images, so headline overlay is safe anywhere.

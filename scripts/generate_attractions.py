import csv
import json
import re
from pathlib import Path

CSV_PATH = Path('google-2025-12-11.csv')
DATA_PATH = Path('_data/attractions.json')
PAGES_DIR = Path('_attractions')

PAGES_DIR.mkdir(exist_ok=True)


def slugify(name: str) -> str:
    normalized = name.strip().lower()
    normalized = normalized.replace('＆', '&').replace('、', '-').replace('，', '-')
    normalized = re.sub(r'[\s]+', '-', normalized)
    normalized = re.sub(r'[^\w\-\u4e00-\u9fff]+', '-', normalized)
    normalized = re.sub(r'-{2,}', '-', normalized)
    normalized = normalized.strip('-')
    return normalized or 'attraction'


def parse_reviews(raw: str):
    cleaned = raw.strip().strip('()').replace(',', '')
    return int(cleaned) if cleaned.isdigit() else None


def main():
    rows = []
    with CSV_PATH.open() as f:
        reader = csv.reader(f)
        rows = list(reader)

    attractions = []
    seen_slugs = set()

    for idx, row in enumerate(rows[2:], start=1):
        if len(row) < 3:
            continue
        name = row[2].strip()
        if not name:
            continue

        slug_base = slugify(name)
        slug = slug_base
        counter = 2
        while slug in seen_slugs:
            slug = f"{slug_base}-{counter}"
            counter += 1
        seen_slugs.add(slug)

        rating_text = row[3].strip()
        rating = float(rating_text) if rating_text else None

        reviews = parse_reviews(row[4]) if len(row) > 4 else None

        category = row[5].strip() if len(row) > 5 else ''
        address = row[9].strip() if len(row) > 9 else ''
        status = row[10].strip() if len(row) > 10 else ''
        hours = row[11].strip() if len(row) > 11 else ''
        image_url = row[12].strip() if len(row) > 12 else ''

        descriptors = [col.strip() for col in row[13:] if col.strip()]
        service = descriptors[0] if descriptors else ''

        attractions.append({
            'slug': slug,
            'name': name,
            'map_url': row[1].strip(),
            'rating': rating,
            'reviews': reviews,
            'category': category,
            'address': address,
            'status': status,
            'hours': hours,
            'image_url': image_url,
            'service': service,
        })

    DATA_PATH.write_text(json.dumps(attractions, ensure_ascii=False, indent=2))

    for item in attractions:
        page_path = PAGES_DIR / f"{item['slug']}.md"
        front_matter_lines = [
            '---',
            'layout: attraction',
            f"title: {item['name']}",
            f"slug: {item['slug']}",
            '---',
            '',
            '<!-- Auto-generated page stub; content is populated via _data/attractions.json -->',
            '',
        ]
        page_path.write_text("\n".join(front_matter_lines))


if __name__ == '__main__':
    main()

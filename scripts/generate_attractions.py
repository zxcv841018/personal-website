from __future__ import annotations
import csv
import re
from pathlib import Path

def slugify(value: str) -> str:
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[\s_-]+", "-", value).strip("-").lower()
    if not value:
        return "spot"
    return value

def main() -> None:
    source = Path("google-2025-12-11.csv")
    target_dir = Path("_attractions")
    target_dir.mkdir(exist_ok=True)

    with source.open(newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    records = []
    slugs: set[str] = set()

    for index, row in enumerate(rows[1:], start=1):
        if len(row) < 3:
            continue
        map_url = row[1].strip()
        title = row[2].strip()
        if not map_url or not title:
            continue

        rating = row[3].strip() if len(row) > 3 else ""
        reviews = row[4].strip("() ") if len(row) > 4 else ""
        category = row[5].strip() if len(row) > 5 else ""
        address = row[9].strip() if len(row) > 9 else ""
        status = row[10].strip() if len(row) > 10 else ""
        hours = row[11].strip("⋅ ") if len(row) > 11 else ""
        image_url = row[12].strip() if len(row) > 12 else ""
        tag = row[13].strip() if len(row) > 13 else ""

        slug_base = slugify(title)
        slug = slug_base
        attempt = 1
        while slug in slugs:
            attempt += 1
            slug = f"{slug_base}-{attempt}"
        slugs.add(slug)

        record = {
            "title": title,
            "slug": slug,
            "map_url": map_url,
            "rating": rating,
            "reviews": reviews,
            "category": category,
            "address": address,
            "status": status,
            "hours": hours,
            "image_url": image_url,
            "tag": tag,
        }
        records.append(record)

    for record in records:
        filename = target_dir / f"{record['slug']}.md"
        front_matter = [
            "---",
            "layout: attraction",
            f"title: {record['title']}",
            f"map_url: {record['map_url']}",
            f"rating: {record['rating']}",
            f"reviews: {record['reviews']}",
            f"category: {record['category']}",
            f"address: {record['address']}",
            f"status: {record['status']}",
            f"hours: {record['hours']}",
            f"image_url: {record['image_url']}",
            f"tag: {record['tag']}",
            "---",
            "",
            "點擊上方的地圖連結即可查看最新資訊。",
        ]
        filename.write_text("\n".join(front_matter), encoding="utf-8")

    print(f"Generated {len(records)} attraction pages in {target_dir}/")

if __name__ == "__main__":
    main()

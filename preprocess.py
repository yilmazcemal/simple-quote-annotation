"""
Preprocess Wayback Machine CSV export into chunked JSON batch files
for the Quote Extraction Labeler.

Usage:
    python preprocess.py "ARCH-1504_2286_web-pages.csv" --batch-size 500
    python preprocess.py "ARCH-1504_2286_web-pages.csv" --batch-size 500 --output-dir batches
"""

import argparse
import csv
import json
import os
import sys


def build_wayback_url(crawl_date: str, original_url: str) -> str:
    """Construct the Wayback Machine URL from crawl date and original URL."""
    crawl_date = crawl_date.strip()
    original_url = original_url.strip()
    return f"https://web.archive.org/web/{crawl_date}/{original_url}"


def preprocess(csv_path: str, batch_size: int, output_dir: str):
    """Read the CSV and write chunked JSON batch files + manifest."""

    if not os.path.isfile(csv_path):
        print(f"Error: CSV file not found: {csv_path}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    # Track batches for the manifest
    manifest = {"source_file": os.path.basename(csv_path), "batch_size": batch_size, "batches": []}

    batch_num = 0
    batch_articles = []
    total_articles = 0

    print(f"Reading CSV: {csv_path}")
    print(f"Batch size: {batch_size}")
    print(f"Output directory: {output_dir}")
    print()

    # Use csv.DictReader to handle quoted fields properly
    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        # The CSV has spaces after commas in headers, so strip them
        reader = csv.DictReader(f, skipinitialspace=True)

        # Normalize fieldnames (strip whitespace)
        reader.fieldnames = [name.strip() for name in reader.fieldnames]

        print(f"CSV columns: {reader.fieldnames}")
        print()

        for row_idx, row in enumerate(reader):
            # Strip whitespace from all values and keys
            row = {k.strip(): (v.strip() if v else "") for k, v in row.items()}

            crawl_date = row.get("crawl_date", "")
            original_url = row.get("url", "")

            article = {
                "article_id": f"art_{total_articles + 1:05d}",
                "crawl_date": crawl_date,
                "last_modified_date": row.get("last_modified_date", ""),
                "domain": row.get("domain", ""),
                "original_url": original_url,
                "wayback_url": build_wayback_url(crawl_date, original_url) if crawl_date and original_url else "",
                "mime_type": row.get("mime_type_web_server", ""),
                "language": row.get("language", ""),
                "content": row.get("content", ""),
            }

            batch_articles.append(article)
            total_articles += 1

            # Write batch when full
            if len(batch_articles) >= batch_size:
                batch_num += 1
                _write_batch(output_dir, batch_num, batch_articles, manifest)
                batch_articles = []

            # Progress
            if total_articles % 5000 == 0:
                print(f"  Processed {total_articles} articles...")

    # Write remaining articles as final batch
    if batch_articles:
        batch_num += 1
        _write_batch(output_dir, batch_num, batch_articles, manifest)

    # Write manifest
    manifest["total_articles"] = total_articles
    manifest["total_batches"] = batch_num

    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print()
    print(f"Done! Processed {total_articles} articles into {batch_num} batch files.")
    print(f"Manifest: {manifest_path}")


def _write_batch(output_dir: str, batch_num: int, articles: list, manifest: dict):
    """Write a single batch file and update manifest."""
    filename = f"batch_{batch_num:03d}.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    file_size_mb = os.path.getsize(filepath) / (1024 * 1024)

    batch_info = {
        "filename": filename,
        "article_count": len(articles),
        "first_article_id": articles[0]["article_id"],
        "last_article_id": articles[-1]["article_id"],
        "file_size_mb": round(file_size_mb, 2),
    }
    manifest["batches"].append(batch_info)

    print(f"  Wrote {filename}: {len(articles)} articles ({file_size_mb:.1f} MB)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess Wayback Machine CSV into batched JSON files")
    parser.add_argument("csv_file", help="Path to the CSV file")
    parser.add_argument("--batch-size", type=int, default=500, help="Number of articles per batch (default: 500)")
    parser.add_argument("--output-dir", default="batches", help="Output directory for batch files (default: batches)")
    args = parser.parse_args()

    preprocess(args.csv_file, args.batch_size, args.output_dir)

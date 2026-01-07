#!/usr/bin/env python3

import sys
import re
import requests
import time
from pathlib import Path
from urllib.parse import urlparse
import unicodedata

# Input

if len(sys.argv) != 2:
    print("Gõ lệnh này: python3 fetch_images.py [tên tệp].md")
    sys.exit(1)

md_path = Path(sys.argv[1]).expanduser().resolve()

def slugify_filename(name: str) -> str:
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "-", name)
    name = name.strip("-")
    return name

slug_name = slugify_filename(md_path.stem)

if slug_name != md_path.stem:
    new_path = md_path.with_name(slug_name + md_path.suffix)
    print(f"Đổi tên tệp: {md_path.name} -> {new_path.name}")
    md_path.rename(new_path)
    md_path = new_path

if not md_path.exists():
    print(f"Không tìm thấy tệp: {md_path}")
    sys.exit(1)

text = md_path.read_text(encoding="utf-8")

# Paths

base_name = md_path.stem
assets_dir = md_path.parent / "assets" / base_name
assets_dir.mkdir(parents=True, exist_ok=True)

md_img = re.compile(r'!\[[^\]]*\]\((https?://[^)]+)\)')
html_img = re.compile(r'<img[^>]+src=["\'](https?://[^"\']+)["\']')

urls = list(dict.fromkeys(md_img.findall(text) + html_img.findall(text)))

if not urls:
    print(f"Tệp này được bỏ qua (Vì không có ảnh hoặc đã tải xong hết từ trước rồi)")
    sys.exit(0)

# Helpers

def ext_from_content_type(ct: str) -> str:
    if not ct:
        return ".img"
    if "jpeg" in ct:
        return ".jpg"
    if "png" in ct:
        return ".png"
    if "webp" in ct:
        return ".webp"
    if "gif" in ct:
        return ".gif"
    return ".img"

def filename_from_url(url: str) -> str | None:
    name = Path(urlparse(url).path).name

    if not name:
        return None

    # URL-encoded hoặc quá dài → bỏ
    if "%" in name or len(name) > 80:
        return None

    if "." in name:
        return name

    return None


# Download

counter = 1

for url in urls:
    filename = filename_from_url(url)

    # Nếu URL không có đuôi = chưa biết tên file
    if filename:
        local_path = assets_dir / filename
        local_ref = f"assets/{base_name}/{filename}"

        # Check images files
        if local_path.exists() and local_path.stat().st_size > 0:
            print(f"Đã có: {filename} nên bỏ qua nhé.")
            text = text.replace(url, local_ref)
            continue

    # Tải ảnh
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
    except Exception as e:
        print(f"⚠ Không tải được {url}: {e}")
        time.sleep(10)
        continue

    # Nếu chưa có filename thì tạo theo content-type
    if not filename:
        ext = ext_from_content_type(r.headers.get("Content-Type", ""))
        filename = f"{base_name}-{counter}{ext}"
        counter += 1

    local_path = assets_dir / filename
    local_ref = f"assets/{base_name}/{filename}"

    if not local_path.exists():
        print(f"Đang tải: {url}")
        local_path.write_bytes(r.content)

    text = text.replace(url, local_ref)

md_path.write_text(text, encoding="utf-8")

print(f"Ảnh đã được lưu tại {assets_dir}")
print("Đã cập nhật đường dẫn trong Markdown")

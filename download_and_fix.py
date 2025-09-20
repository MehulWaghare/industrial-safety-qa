import os
import requests
import json
from urllib.parse import urlparse

# Folder where PDFs will be stored
PDF_DIR = "data/industrial-safety-pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

# Load sources
with open("sources.json", "r", encoding="utf-8") as f:
    sources = json.load(f)

corrected = []

for src in sources:
    url = src["url"]
    title = src["title"]

    # Extract filename from URL
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)

    # Force .pdf extension if missing
    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"

    filepath = os.path.join(PDF_DIR, filename)

    # Download if not already present
    if not os.path.exists(filepath):
        print(f"⬇️ Downloading: {title}")
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(filepath, "wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
        else:
            print(f"⚠️ Failed to download {url}")

    corrected.append({
        "file": filename,
        "title": title,
        "url": url
    })

# Save corrected JSON
with open("sources_corrected.json", "w", encoding="utf-8") as f:
    json.dump(corrected, f, indent=2, ensure_ascii=False)

print("✅ Done! All PDFs stored in", PDF_DIR)
print("✅ sources_corrected.json generated.")

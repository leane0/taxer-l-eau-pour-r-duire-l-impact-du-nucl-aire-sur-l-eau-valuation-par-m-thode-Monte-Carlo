#!/usr/bin/env python3

import json
import hashlib
from pathlib import Path

import requests
from bs4 import BeautifulSoup

STATE_FILE = "edf_monitor_state.json"

SITES = {
    "Tricastin": "https://www.edf.fr/la-centrale-nucleaire-du-tricastin/l-exploitation-de-la-centrale-nucleaire-du-tricastin",
    "Cruas": "https://www.edf.fr/la-centrale-nucleaire-de-cruas-meysse/l-exploitation-de-la-centrale-nucleaire-de-cruas-meysse",
    "Saint-Alban": "https://www.edf.fr/la-centrale-nucleaire-de-saint-alban-saint-maurice/l-exploitation-de-la-centrale-nucleaire-de-saint-alban",
    "Bugey": "https://www.edf.fr/la-centrale-nucleaire-du-bugey/l-exploitation-de-la-centrale-nucleaire-du-bugey",
    "Creys-Malville": "https://www.edf.fr/la-centrale-nucleaire-de-creys-malville/le-demantelement-de-la-centrale-nucleaire-de-creys-malville",
    "Golfech": "https://www.edf.fr/la-centrale-nucleaire-de-golfech/l-exploitation-de-la-centrale-nucleaire-de-golfech",
    "Blayais": "https://www.edf.fr/la-centrale-nucleaire-du-blayais/l-exploitation-de-la-centrale-nucleaire-du-blayais",
    "Civaux": "https://www.edf.fr/la-centrale-nucleaire-de-civaux/l-exploitation-de-la-centrale-nucleaire-de-civaux",
    "Chinon": "https://www.edf.fr/la-centrale-nucleaire-de-chinon/l-exploitation-de-la-centrale-nucleaire-de-chinon",
    "Saint-Laurent": "https://www.edf.fr/la-centrale-nucleaire-de-saint-laurent/l-exploitation-de-la-centrale-nucleaire-de-saint-laurent",
    "Dampierre": "https:/ /www.edf.fr/la-centrale-nucleaire-de-dampierre-en-burly/l-exploitation-de-la-centrale-nucleaire-de-dampierre",
    "Belleville": "https://www.edf.fr/la-centrale-nucleaire-de-belleville/l-exploitation-de-la-centrale-nucleaire-de-belleville",
    "Nogent": "https://www.edf.fr/la-centrale-nucleaire-de-nogent-sur-seine/l-exploitation-de-la-centrale-nucleaire-de-nogent",
    "Cattenom": "https://www.edf.fr/la-centrale-nucleaire-de-cattenom/l-exploitation-de-la-centrale-nucleaire-de-cattenom",
    "Chooz": "https://www.edf.fr/la-centrale-nucleaire-de-chooz/l-exploitation-de-la-centrale-nucleaire-de-chooz",
}


def load_state():
    path = Path(STATE_FILE)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def normalize_text(text):
    return " ".join(text.split())


def extract_download_blocks(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    blocks = soup.select("div.file-download.surface-01")

    result = []

    for block in blocks:
        text = normalize_text(block.get_text(" ", strip=True))

        links = [
            {
                "text": normalize_text(a.get_text(" ", strip=True)),
                "href": a.get("href", ""),
            }
            for a in block.find_all("a")
        ]

        result.append(
            {
                "text": text,
                "links": links,
                "html_hash": hashlib.sha256(
                    str(block).encode("utf-8")
                ).hexdigest(),
            }
        )

    return result


def compare_blocks(old_blocks, new_blocks):
    changes = []

    old_map = {b["html_hash"]: b for b in old_blocks}
    new_map = {b["html_hash"]: b for b in new_blocks}

    added = set(new_map) - set(old_map)
    removed = set(old_map) - set(new_map)

    for h in added:
        changes.append(
            {
                "type": "ADDED",
                "content": new_map[h]["text"],
            }
        )

    for h in removed:
        changes.append(
            {
                "type": "REMOVED",
                "content": old_map[h]["text"],
            }
        )

    return changes


def main():
    previous_state = load_state()
    current_state = {}

    all_changes = {}

    for site_name, url in SITES.items():
        print(f"Checking {site_name}...")

        try:
            blocks = extract_download_blocks(url)

            current_state[site_name] = {
                "url": url,
                "blocks": blocks,
            }

            if site_name in previous_state:
                changes = compare_blocks(
                    previous_state[site_name]["blocks"],
                    blocks,
                )

                if changes:
                    all_changes[site_name] = changes

        except Exception as e:
            print(f"ERROR on {site_name}: {e}")

    if not previous_state:
        save_state(current_state)
        print("\nInitial snapshot created.")
        return

    if not all_changes:
        print("\nNo changes detected.")
    else:
        print("\nChanges detected:\n")

        for site, changes in all_changes.items():
            print("=" * 80)
            print(site)

            for change in changes:
                print(f"\n[{change['type']}]")
                print(change["content"][:500])

    save_state(current_state)


if __name__ == "__main__":
    main()
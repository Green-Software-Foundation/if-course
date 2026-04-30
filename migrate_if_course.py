#!/usr/bin/env python3
"""
Migration script: Impact Framework course markdown -> Mighty Networks course lessons.

Modes:
  Default          : create all lessons (first run)
  UPDATE_IMAGES=true : fetch existing lessons by title and PATCH the ones with images
"""

import os
import re
import sys
import time
import glob

import requests
import markdown


GITHUB_RAW_BASE = (
    "https://raw.githubusercontent.com/Green-Software-Foundation/if-course/main/images/"
)


def derive_title(filename: str) -> str:
    name = os.path.basename(filename)
    name = re.sub(r"^\d+\.", "", name)
    name = name.removesuffix(".md")
    name = name.replace("-", " ")
    return name.title()


def rewrite_image_urls(text: str) -> str:
    """Replace local ./images/ or images/ src with GitHub raw URL."""
    return re.sub(
        r"!\[([^\]]*)\]\(\.?/?images/([^)]+)\)",
        lambda m: f"![{m.group(1)}]({GITHUB_RAW_BASE}{m.group(2)})",
        text,
    )


def md_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["fenced_code", "tables"],
    )


def collect_lessons(repo_root: str) -> list[dict]:
    pattern = os.path.join(repo_root, "[0-9]*.md")
    files = glob.glob(pattern)
    files.sort(key=lambda f: int(re.match(r"(\d+)\.", os.path.basename(f)).group(1)))
    lessons = []
    for position, filepath in enumerate(files, start=1):
        with open(filepath, encoding="utf-8") as fh:
            raw = fh.read()
        has_images = bool(re.search(r"!\[.*?\]\(\.?/?images/", raw))
        raw = rewrite_image_urls(raw)
        html = md_to_html(raw)
        lessons.append(
            {
                "title": derive_title(filepath),
                "body": html,
                "position": position,
                "source_file": os.path.basename(filepath),
                "has_images": has_images,
            }
        )
    return lessons


def post_lesson(session, api_base, network_id, space_id, lesson) -> bool:
    url = f"{api_base}/networks/{network_id}/spaces/{space_id}/courseworks"
    payload = {"type": "lesson", "title": lesson["title"], "description": lesson["body"]}
    response = session.post(url, json=payload)
    if response.ok:
        return True
    print(
        f"\n  ERROR [{lesson['position']}] '{lesson['title']}' — "
        f"HTTP {response.status_code}: {response.text[:200]}"
    )
    return False


def fetch_existing_courseworks(session, api_base, network_id, space_id) -> dict:
    """Return a title -> coursework_id mapping for all existing lessons."""
    url = f"{api_base}/networks/{network_id}/spaces/{space_id}/courseworks"
    response = session.get(url)
    if not response.ok:
        sys.exit(f"ERROR fetching existing courseworks: HTTP {response.status_code}: {response.text[:200]}")
    data = response.json()
    print(f"\n  [DEBUG] GET {url}")
    print(f"  [DEBUG] response keys: {list(data.keys()) if isinstance(data, dict) else f'list of {len(data)}'}")
    if isinstance(data, dict):
        for k, v in data.items():
            print(f"  [DEBUG]   {k!r}: {str(v)[:120]}")
    # handle both {"courseworks": [...]} and plain list
    items = data if isinstance(data, list) else data.get("courseworks", data.get("data", []))
    return {item["title"]: item["id"] for item in items}


def patch_lesson(session, api_base, network_id, space_id, coursework_id, lesson) -> bool:
    url = f"{api_base}/networks/{network_id}/spaces/{space_id}/courseworks/{coursework_id}"
    payload = {"description": lesson["body"]}
    response = session.patch(url, json=payload)
    if response.ok:
        return True
    print(
        f"\n  ERROR [{lesson['position']}] '{lesson['title']}' — "
        f"HTTP {response.status_code}: {response.text[:200]}"
    )
    return False


def main() -> None:
    api_token = os.environ.get("MN_API_TOKEN", "")
    network_id = os.environ.get("MN_NETWORK_ID", "")
    space_id = os.environ.get("MN_SPACE_ID", "23617101")
    dry_run = os.environ.get("DRY_RUN", "").lower() == "true"
    update_images = os.environ.get("UPDATE_IMAGES", "").lower() == "true"

    if not dry_run:
        if not api_token:
            sys.exit("ERROR: MN_API_TOKEN is required (or set DRY_RUN=true)")
        if not network_id:
            sys.exit("ERROR: MN_NETWORK_ID is required (or set DRY_RUN=true)")

    repo_root = os.path.dirname(os.path.abspath(__file__))
    lessons = collect_lessons(repo_root)

    if update_images:
        lessons_to_process = [l for l in lessons if l["has_images"]]
        mode_label = "UPDATE IMAGES"
    else:
        lessons_to_process = lessons
        mode_label = "DRY RUN" if dry_run else "MIGRATE"

    print(f"[{mode_label}] {len(lessons_to_process)} lesson(s) to process")
    print(f"  Network ID : {network_id or '<not set>'}")
    print(f"  Space ID   : {space_id}")
    print()

    for lesson in lessons_to_process:
        tag = " [has images]" if lesson["has_images"] else ""
        print(f"  [{lesson['position']:>2}] {lesson['source_file']:<50} -> '{lesson['title']}'{tag}")

    print()

    if dry_run:
        print("[DRY RUN] No API calls made.")
        return

    api_base = "https://api.mn.co/admin/v1"
    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    )

    updated = created = failed = 0

    if update_images:
        print("  Fetching existing courseworks ... ", end="", flush=True)
        existing = fetch_existing_courseworks(session, api_base, network_id, space_id)
        print(f"found {len(existing)}")
        print()
        for lesson in lessons_to_process:
            cw_id = existing.get(lesson["title"])
            if not cw_id:
                print(f"  [{lesson['position']:>2}] '{lesson['title']}' — not found in space, skipping")
                failed += 1
                continue
            print(f"  Patching [{lesson['position']:>2}] '{lesson['title']}' (id={cw_id}) ... ", end="", flush=True)
            if patch_lesson(session, api_base, network_id, space_id, cw_id, lesson):
                updated += 1
                print("OK")
            else:
                failed += 1
            time.sleep(0.5)
        print()
        print("=" * 50)
        print(f"Image fix complete: {updated} updated, {failed} failed")
    else:
        for lesson in lessons_to_process:
            print(f"  Posting [{lesson['position']:>2}/{len(lessons_to_process)}] '{lesson['title']}' ... ", end="", flush=True)
            if post_lesson(session, api_base, network_id, space_id, lesson):
                created += 1
                print("OK")
            else:
                failed += 1
            time.sleep(0.5)
        print()
        print("=" * 50)
        print(f"Migration complete: {created} created, {failed} failed")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()

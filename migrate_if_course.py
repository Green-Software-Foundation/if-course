#!/usr/bin/env python3
"""
Migration script: Impact Framework course markdown -> Mighty Networks course lessons.
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
    """'7.sci-walkthrough-operational-energy.md' -> 'Sci Walkthrough Operational Energy'"""
    name = os.path.basename(filename)
    name = re.sub(r"^\d+\.", "", name)   # strip leading "N."
    name = name.removesuffix(".md")
    name = name.replace("-", " ")
    return name.title()


def rewrite_image_urls(text: str) -> str:
    """Replace local images/foo.png src with GitHub raw URL."""
    return re.sub(
        r"!\[([^\]]*)\]\(images/([^)]+)\)",
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
        raw = rewrite_image_urls(raw)
        html = md_to_html(raw)
        lessons.append(
            {
                "title": derive_title(filepath),
                "body": html,
                "position": position,
                "source_file": os.path.basename(filepath),
            }
        )
    return lessons


def post_lesson(
    session: requests.Session,
    api_base: str,
    network_id: str,
    space_id: str,
    lesson: dict,
) -> bool:
    url = f"{api_base}/networks/{network_id}/spaces/{space_id}/courseworks"
    payload = {
        "type": "lesson",
        "title": lesson["title"],
        "body": lesson["body"],
        "position": lesson["position"],
    }
    response = session.post(url, json=payload)
    if response.ok:
        return True
    print(
        f"  ERROR [{lesson['position']}] '{lesson['title']}' — "
        f"HTTP {response.status_code}: {response.text[:200]}"
    )
    return False


def main() -> None:
    api_token = os.environ.get("MN_API_TOKEN", "")
    network_id = os.environ.get("MN_NETWORK_ID", "")
    space_id = os.environ.get("MN_SPACE_ID", "23617101")
    dry_run = os.environ.get("DRY_RUN", "").lower() == "true"

    if not dry_run:
        if not api_token:
            sys.exit("ERROR: MN_API_TOKEN is required (or set DRY_RUN=true)")
        if not network_id:
            sys.exit("ERROR: MN_NETWORK_ID is required (or set DRY_RUN=true)")

    repo_root = os.path.dirname(os.path.abspath(__file__))
    lessons = collect_lessons(repo_root)

    print(f"{'[DRY RUN] ' if dry_run else ''}Found {len(lessons)} lessons to migrate")
    print(f"  Network ID : {network_id or '<not set>'}")
    print(f"  Space ID   : {space_id}")
    print()

    for lesson in lessons:
        print(
            f"  [{lesson['position']:>2}] {lesson['source_file']:<50} -> '{lesson['title']}'"
        )

    print()

    if dry_run:
        print("[DRY RUN] No API calls made. Set DRY_RUN=false and provide real credentials to migrate.")
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

    created = 0
    failed = 0

    for lesson in lessons:
        print(f"  Posting [{lesson['position']:>2}/{len(lessons)}] '{lesson['title']}' ... ", end="", flush=True)
        success = post_lesson(session, api_base, network_id, space_id, lesson)
        if success:
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

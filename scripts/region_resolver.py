#!/usr/bin/env python3
"""Region resolution for GEO-SEO AI Agent.

Detects target market region from URL and page content, loads region
profiles from regions/profiles.yaml.

Usage:
    python3 scripts/region_resolver.py detect <url> [content_file]
    python3 scripts/region_resolver.py profile <region_code>
"""

import sys
import os
import re
import yaml
from urllib.parse import urlparse


PROFILES_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "regions", "profiles.yaml")


def load_profiles():
    """Load all region profiles from profiles.yaml."""
    if not os.path.exists(PROFILES_PATH):
        return {"regions": {}}
    with open(PROFILES_PATH) as f:
        return yaml.safe_load(f)


def load_profile(region_code):
    """Load a single region profile by code. Returns None if not found."""
    profiles = load_profiles()
    for r in profiles.get("regions", {}).values():
        if r["code"] == region_code:
            return r
    return None


def list_regions():
    """Return list of available region codes and labels."""
    profiles = load_profiles()
    return [(r["code"], r["label"]) for r in profiles.get("regions", {}).values()]


def detect_tld(url):
    """Detect region from URL TLD / domain suffix."""
    domain = urlparse(url).netloc or urlparse(url).path
    domain = domain.lower()
    profiles = load_profiles()
    for r in profiles.get("regions", {}).values():
        for tld in r.get("tlds", []):
            if domain.endswith(tld):
                return r["code"]
    return None


def extract_lang_tags(content):
    """Extract language codes from HTML lang attributes and URL patterns."""
    if not content:
        return set()
    lang_tags = set()
    for m in re.finditer(r'lang="([a-z]{2}(?:-[a-z]{2,3})?)"', content.lower()):
        lang_tags.add(m.group(1).split("-")[0])
    for m in re.finditer(r"lang='([a-z]{2}(?:-[a-z]{2,3})?)'", content.lower()):
        lang_tags.add(m.group(1).split("-")[0])
    for m in re.finditer(r'href="[^"]*/([a-z]{2}(?:-[a-z]{2,3})?)/', content.lower()):
        lang_tags.add(m.group(1).split("-")[0])
    for m in re.finditer(r"href='[^']*/([a-z]{2}(?:-[a-z]{2,3})?)/", content.lower()):
        lang_tags.add(m.group(1).split("-")[0])
    return lang_tags


def detect_language(content):
    """Detect language from page content. Returns language code or None."""
    if not content:
        return None

    cjk_chars = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
    total_chars = len(content.strip())

    if total_chars > 0:
        cjk_ratio = cjk_chars / total_chars
        if cjk_ratio > 0.05:
            return "zh"

    has_zh_lang = any(tag in content.lower() for tag in [
        'lang="zh"', "lang='zh'", 'lang="zh-cn"', "lang='zh-cn'",
        'lang="zh-hans"', "lang='zh-hans'", 'lang="zh-hant"', "lang='zh-hant'",
    ])
    if has_zh_lang:
        return "zh"

    return None


def detect_multi_lang(content):
    """Detect if content indicates a multi-language setup."""
    if not content:
        return False
    lang_codes = extract_lang_tags(content)
    relevant = {lc for lc in lang_codes if lc in ("en", "zh")}
    return len(relevant) > 1


def detect(url, content=None):
    """Detect region from URL and optional page content.

    Returns:
        str: Region code, "multi" for ambiguous multi-language, or "global" default.
    """
    # 1. Explicit TLD detection
    tld_result = detect_tld(url)
    if tld_result:
        return tld_result

    # 2. Content-based detection
    if content:
        lang_result = detect_language(content)
        if lang_result == "zh":
            return "cn"

        if detect_multi_lang(content):
            return "multi"

    # 4. Default
    return "global"


def format_ask_message(url, detected_status):
    """Format the user-facing message when detection is ambiguous."""
    if detected_status == "multi":
        return (
            f"Detected multiple languages for {url}. "
            "How would you like to proceed?\n"
            "1. Global audit only\n"
            "2. Global + China regional audit\n"
            "3. China regional audit only\n"
            "(Enter 1, 2, or 3)"
        )
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 region_resolver.py detect <url> [content_file]", file=sys.stderr)
        print("       python3 region_resolver.py profile <region_code>", file=sys.stderr)
        print("       python3 region_resolver.py list", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == "detect":
        if len(sys.argv) < 3:
            print("Missing URL argument", file=sys.stderr)
            sys.exit(1)
        url = sys.argv[2]
        content = None
        if len(sys.argv) >= 4:
            content_file = sys.argv[3]
            if os.path.exists(content_file):
                with open(content_file) as f:
                    content = f.read()
        result = detect(url, content)
        print(result)

    elif command == "profile":
        if len(sys.argv) < 3:
            print("Missing region code", file=sys.stderr)
            sys.exit(1)
        profile = load_profile(sys.argv[2])
        if profile:
            print(yaml.dump(profile, default_flow_style=False))
        else:
            available = ", ".join(f"'{c}'" for c, _ in list_regions())
            print(f"Error: Region '{sys.argv[2]}' not found. Available: {available}", file=sys.stderr)
            sys.exit(1)

    elif command == "list":
        for code, label in list_regions():
            print(f"{code:12s} {label}")

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Use: detect, profile, list", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

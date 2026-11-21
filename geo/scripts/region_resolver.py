#!/usr/bin/env python3
"""Region resolution for GEO-SEO AI Agent.

Detects target market region from URL and page content, loads region
profiles from the self-located ``regions/profiles.yaml`` of the geo skill,
and lists the CN-only guidance that must be loaded for ``--region cn``.

Usage:
    python3 geo/scripts/region_resolver.py detect <url> [content_file]
    python3 geo/scripts/region_resolver.py profile <region_code>
    python3 geo/scripts/region_resolver.py guidance <region_code>
    python3 geo/scripts/region_resolver.py list
"""

import json
import os
import re
import sys
from urllib.parse import urlparse

# Region files ship inside the SKILL.md-bearing geo skill so npx copies them.
# Ordered from the script's own directory; the first existing candidate wins.
REGION_SEARCH_DIRS = ("..", "../..", "../../..")
MANIFEST_REL = os.path.join("regions", "cn-variants.json")


def resolve_region_file(relative_path):
    """Find *relative_path* below an ordered set of geo-skill roots."""
    base = os.path.dirname(os.path.abspath(__file__))
    for suffix in REGION_SEARCH_DIRS:
        candidate = os.path.normpath(os.path.join(base, suffix, relative_path))
        if os.path.isfile(candidate):
            return candidate
    return None


def resolve_profiles_path():
    """Return the located profiles.yaml, or None when no candidate exists."""
    return resolve_region_file(os.path.join("regions", "profiles.yaml"))


def _parse_scalar(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [_parse_scalar(item) for item in inner.split(",")] if inner else []
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    if value in ("null", "~"):
        return None
    return value


def _parse_node(lines, index, indent):
    if index >= len(lines):
        return None, index
    if lines[index][1].startswith("- "):
        return _parse_list(lines, index, indent)
    return _parse_map(lines, index, indent)


def _parse_map(lines, index, indent):
    result = {}
    while index < len(lines):
        current_indent, content = lines[index]
        if current_indent < indent or content.startswith("- "):
            break
        if current_indent > indent:
            index += 1
            continue
        key, _, raw = content.partition(":")
        raw = raw.strip()
        index += 1
        if raw in (">", ">-", "|", "|-"):
            block = []
            while index < len(lines) and lines[index][0] > indent:
                block.append(lines[index][1])
                index += 1
            separator = " " if raw.startswith(">") else "\n"
            result[key.strip()] = separator.join(block) + ("\n" if raw.startswith(">") else "")
        elif raw == "":
            if index < len(lines) and lines[index][0] > indent:
                result[key.strip()], index = _parse_node(lines, index, lines[index][0])
            else:
                result[key.strip()] = None
        else:
            result[key.strip()] = _parse_scalar(raw)
    return result, index


def _parse_list(lines, index, indent):
    result = []
    while index < len(lines):
        current_indent, content = lines[index]
        if current_indent < indent or not content.startswith("- "):
            break
        item_text = content[2:].strip()
        index += 1
        if ":" in item_text and not item_text.startswith(("'", '"')):
            item = {}
            key, _, raw = item_text.partition(":")
            raw = raw.strip()
            if raw == "":
                if index < len(lines) and lines[index][0] > indent:
                    item[key.strip()], index = _parse_node(lines, index, lines[index][0])
                else:
                    item[key.strip()] = None
            else:
                item[key.strip()] = _parse_scalar(raw)
            while index < len(lines) and lines[index][0] > indent and not lines[index][1].startswith("- "):
                child_indent, child = lines[index]
                key, _, raw = child.partition(":")
                raw = raw.strip()
                index += 1
                if raw == "" and index < len(lines) and lines[index][0] > child_indent:
                    item[key.strip()], index = _parse_node(lines, index, lines[index][0])
                else:
                    item[key.strip()] = _parse_scalar(raw)
            result.append(item)
        else:
            result.append(_parse_scalar(item_text))
    return result, index


def _parse_profiles(text):
    """Parse the small YAML subset used by profiles.yaml (stdlib only)."""
    lines = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        lines.append((len(raw) - len(raw.lstrip(" ")), stripped))
    result, _ = _parse_node(lines, 0, lines[0][0] if lines else 0)
    return result if isinstance(result, dict) else {}


def load_profiles():
    """Load all region profiles from the self-located profiles.yaml."""
    path = resolve_profiles_path()
    if path is None:
        return {"regions": {}}
    with open(path, encoding="utf-8") as handle:
        return _parse_profiles(handle.read())


def load_manifest():
    """Load the CN manifest shipped beside profiles.yaml."""
    path = resolve_region_file(MANIFEST_REL)
    if path is None:
        return {}
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def load_profile(region_code):
    """Load a single region profile by code. Returns None if not found."""
    profiles = load_profiles()
    for region in profiles.get("regions", {}).values():
        if region["code"] == region_code:
            return region
    return None


def list_regions():
    """Return list of available region codes and labels."""
    profiles = load_profiles()
    return [(region["code"], region["label"]) for region in profiles.get("regions", {}).values()]


def detect_tld(url):
    """Detect region from URL TLD / domain suffix."""
    domain = (urlparse(url).netloc or urlparse(url).path).lower()
    profiles = load_profiles()
    for region in profiles.get("regions", {}).values():
        for tld in region.get("tlds", []):
            if domain.endswith(tld):
                return region["code"]
    return None


def extract_lang_tags(content):
    """Extract language codes from HTML lang attributes and URL patterns."""
    if not content:
        return set()
    lang_tags = set()
    for pattern in (
        r'lang="([a-z]{2}(?:-[a-z]{2,3})?)"',
        r"lang='([a-z]{2}(?:-[a-z]{2,3})?)'",
        r'href="[^"]*/([a-z]{2}(?:-[a-z]{2,3})?)/',
        r"href='[^']*/([a-z]{2}(?:-[a-z]{2,3})?)/",
    ):
        for match in re.finditer(pattern, content.lower()):
            lang_tags.add(match.group(1).split("-")[0])
    return lang_tags


def detect_language(content):
    """Detect language from page content. Returns language code or None."""
    if not content:
        return None

    cjk_chars = sum(1 for char in content if "\u4e00" <= char <= "\u9fff")
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
    relevant = {code for code in lang_codes if code in ("en", "zh")}
    return len(relevant) > 1


def detect(url, content=None):
    """Detect region from URL and optional page content.

    Returns:
        str: Region code, "multi" for ambiguous multi-language, or "global" default.
    """
    tld_result = detect_tld(url)
    if tld_result:
        return tld_result

    if content:
        lang_result = detect_language(content)
        if lang_result == "zh":
            return "cn"
        if detect_multi_lang(content):
            return "multi"

    return "global"


def guidance_files(region_code):
    """Return CN-only guidance paths, or [] for any non-CN region.

    Paths are relative to the geo skill root; CN variants are sibling skills.
    """
    if region_code != "cn":
        return []
    manifest = load_manifest()
    files = list(manifest.get("knowledge_base", []))
    variant_file = manifest.get("variant_file", "SKILL.cn.md")
    files.extend(f"../{name}/{variant_file}" for name in manifest.get("variants", []))
    return files


def geo_root():
    """Return the geo skill root that owns the located profiles.yaml."""
    profiles = resolve_profiles_path()
    if profiles is None:
        return None
    return os.path.dirname(os.path.dirname(profiles))


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
        print("       python3 region_resolver.py guidance <region_code>", file=sys.stderr)
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
                with open(content_file, encoding="utf-8") as handle:
                    content = handle.read()
        print(detect(url, content))

    elif command == "profile":
        if len(sys.argv) < 3:
            print("Missing region code", file=sys.stderr)
            sys.exit(1)
        profile = load_profile(sys.argv[2])
        if profile:
            print(json.dumps(profile, indent=2, ensure_ascii=False))
        else:
            available = ", ".join(f"'{code}'" for code, _ in list_regions())
            print(f"Error: Region '{sys.argv[2]}' not found. Available: {available}", file=sys.stderr)
            sys.exit(1)

    elif command == "guidance":
        if len(sys.argv) < 3:
            print("Missing region code", file=sys.stderr)
            sys.exit(1)
        region_code = sys.argv[2]
        if region_code != "cn" and load_profile(region_code) is None:
            available = ", ".join(f"'{code}'" for code, _ in list_regions())
            print(f"Error: Region '{region_code}' not found. Available: {available}", file=sys.stderr)
            sys.exit(1)
        root = geo_root()
        files = guidance_files(region_code)
        missing = [path for path in files if root is None or not os.path.isfile(os.path.normpath(os.path.join(root, path)))]
        if missing:
            print("Error: CN guidance files missing from install: " + ", ".join(missing), file=sys.stderr)
            sys.exit(1)
        for path in files:
            print(path)

    elif command == "list":
        for code, label in list_regions():
            print(f"{code:12s} {label}")

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Use: detect, profile, guidance, list", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

"""Characterization tests for the additive bot-UA fetch capability.

Locks in two behaviours introduced for the GEO audit UA-dependent-rendering fix:

1. ``fetch_page(url, user_agent=...)`` sends the requested User-Agent header.
   A known ``AI_CRAWLERS`` key resolves to that crawler's UA string; an unknown
   name (or a raw UA string) is passed through / falls back without a KeyError.
   The default call path is byte-for-byte unchanged (uses ``DEFAULT_HEADERS``).

2. The additive CLI ``bot <crawler>`` mode emits the same JSON shape as ``page``
   plus a ``user_agent`` echo field that exists ONLY in the bot wrapper (never in
   the ``fetch_page()`` result dict).
"""

import json
import os
import runpy
import sys
from unittest.mock import MagicMock, patch

import pytest
import requests

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "skills", "geo", "scripts")
)

from fetch_page import AI_CRAWLERS, DEFAULT_HEADERS, fetch_page  # noqa: E402

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FETCH_PAGE_PATH = os.path.join(REPO_ROOT, "skills", "geo", "scripts", "fetch_page.py")
BASE_URL = "https://example.com/"
PAGE_HTML = "<html><head><title>T</title></head><body><h1>Hello</h1><p>body</p></body></html>"


def _make_response(html=PAGE_HTML, status_code=200):
    resp = MagicMock()
    resp.status_code = status_code
    resp.text = html
    resp.history = []
    resp.headers = {}
    resp.url = BASE_URL
    return resp


# --- 1. fetch_page(user_agent=...) sends the requested UA -------------------


def test_fetch_page_sends_known_crawler_ua():
    """A known AI_CRAWLERS key resolves to that crawler's UA string."""
    expected_ua = AI_CRAWLERS["GPTBot"]
    with patch("fetch_page.requests.get", return_value=_make_response()) as mock_get:
        fetch_page(BASE_URL, user_agent="GPTBot")
    kwargs = mock_get.call_args.kwargs
    assert kwargs["headers"]["User-Agent"] == expected_ua


def test_fetch_page_sends_raw_ua_string():
    """A raw UA string is used verbatim (not looked up in AI_CRAWLERS)."""
    raw_ua = "MyCustomBot/1.0 (+https://example.com/bot)"
    with patch("fetch_page.requests.get", return_value=_make_response()) as mock_get:
        fetch_page(BASE_URL, user_agent=raw_ua)
    kwargs = mock_get.call_args.kwargs
    assert kwargs["headers"]["User-Agent"] == raw_ua


def test_fetch_page_unknown_name_falls_back_without_keyerror():
    """An unknown crawler name falls back to DEFAULT_HEADERS, no KeyError."""
    with patch("fetch_page.requests.get", return_value=_make_response()) as mock_get:
        result = fetch_page(BASE_URL, user_agent="DefinitelyNotACrawler")
    assert result["status_code"] == 200
    kwargs = mock_get.call_args.kwargs
    assert kwargs["headers"]["User-Agent"] == DEFAULT_HEADERS["User-Agent"]


def test_fetch_page_default_unchanged():
    """Default call path still uses DEFAULT_HEADERS exactly."""
    with patch("fetch_page.requests.get", return_value=_make_response()) as mock_get:
        fetch_page(BASE_URL)
    kwargs = mock_get.call_args.kwargs
    assert kwargs["headers"] == DEFAULT_HEADERS


def test_fetch_page_result_has_no_user_agent_key():
    """The user_agent echo must NEVER be added to the fetch_page() result dict."""
    with patch("fetch_page.requests.get", return_value=_make_response()):
        result = fetch_page(BASE_URL, user_agent="GPTBot")
    assert "user_agent" not in result


# --- 2. CLI `bot <crawler>` mode -------------------------------------------


def _run_cli(capsys, monkeypatch, *argv):
    def fake_get(url, **_kwargs):
        return _make_response()

    monkeypatch.setattr(requests, "get", fake_get)
    monkeypatch.setattr(sys, "argv", ["fetch_page.py", *argv])
    exit_exc = None
    try:
        runpy.run_path(FETCH_PAGE_PATH, run_name="__main__")
    except SystemExit as exc:
        exit_exc = exc
    captured = capsys.readouterr()
    return captured, exit_exc


def test_cli_bot_mode_emits_page_shape_plus_user_agent(capsys, monkeypatch):
    """`bot GPTBot` emits the page JSON shape plus a user_agent echo field."""
    captured, exit_exc = _run_cli(capsys, monkeypatch, BASE_URL, "bot", "GPTBot")
    assert exit_exc is None or exit_exc.code == 0
    data = json.loads(captured.out)
    # Same core keys as page mode.
    for key in (
        "url",
        "status_code",
        "title",
        "description",
        "canonical",
        "h1_tags",
        "word_count",
        "has_ssr_content",
        "errors",
        "structured_data",
        "security_headers",
    ):
        assert key in data, f"missing page-shape key: {key}"
    assert data["user_agent"] == AI_CRAWLERS["GPTBot"]


def test_cli_page_mode_has_no_user_agent_echo(capsys, monkeypatch):
    """`page` mode must NOT gain a user_agent echo field."""
    captured, exit_exc = _run_cli(capsys, monkeypatch, BASE_URL, "page")
    assert exit_exc is None or exit_exc.code == 0
    data = json.loads(captured.out)
    assert "user_agent" not in data

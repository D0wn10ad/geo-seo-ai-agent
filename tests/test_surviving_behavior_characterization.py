"""Characterization of behavior that MUST survive the npx-skills migration.

Pins CURRENT observable behavior only:
  * fetch_page.py CLI stdout (parsed JSON / literal text) and exit status for
    every mode: page, robots, llms, sitemap, blocks, full;
  * robots.txt Cloudflare-managed detection as emitted on CLI stdout;
  * webapp region_label fallback (region -> country) and the rendered HTML of
    the dashboard / prospect pages (region-aware output).

Deliberately NOT tested here: installer internals slated for deletion
(clone/pull/copy_tree/copy_files/rewrite). Those are catalogued in the evidence
file, not pinned by these tests.

HTTP responses come from fixed in-process fixtures (requests.get is patched),
so these tests are deterministic and network-independent. The module under test
can be redirected with GEO_CHAR_FETCH_PAGE_PATH / GEO_CHAR_WEBAPP_APP_PATH so a
deliberate-break sensitivity run can point at a throwaway copy.
"""

import importlib.util
import json
import os
import runpy
import sys
from pathlib import Path

import pytest
import requests

pytestmark = pytest.mark.filterwarnings("ignore::bs4.XMLParsedAsHTMLWarning")

REPO_ROOT = Path(__file__).resolve().parents[1]
_FETCH_PAGE_DEFAULT = REPO_ROOT / "scripts" / "fetch_page.py"
_WEBAPP_DEFAULT = REPO_ROOT / "scripts" / "webapp" / "app.py"
_TEMPLATES = REPO_ROOT / "scripts" / "webapp" / "templates"
_BASE_URL = "https://example.com/"


def _fetch_page_path():
    return Path(os.environ.get("GEO_CHAR_FETCH_PAGE_PATH", str(_FETCH_PAGE_DEFAULT)))


def _webapp_path():
    return Path(os.environ.get("GEO_CHAR_WEBAPP_APP_PATH", str(_WEBAPP_DEFAULT)))


class _Response:
    def __init__(self, text="", status_code=200, headers=None, url=""):
        self.text = text
        self.status_code = status_code
        self.headers = headers if headers is not None else {}
        self.url = url
        self.history = []


PAGE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <title>Characterization Corp — Home</title>
  <meta name="description" content="A fixed fixture page used for behavior characterization.">
  <link rel="canonical" href="https://example.com/">
  <script type="application/ld+json">{"@type":"Organization","name":"Characterization Corp"}</script>
</head>
<body>
  <h1>Characterization Corp</h1>
  <p>Alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi
  omicron pi rho sigma tau upsilon phi chi psi omega. Extra words keep the
  word count well above the two hundred Word threshold only in the SSR fixture;
  here plain server-rendered text is already sufficient for this assertion.</p>
  <a href="/about">About</a>
  <a href="https://external.test/reference">External reference</a>
  <img src="/logo.png" alt="Logo">
</body>
</html>"""

ROBOTS_CLOUDFLARE = """# BEGIN Cloudflare Managed content

User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

# END Cloudflare Managed Content

User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
"""

ROBOTS_PLAIN = """User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
"""

SITEMAP_XML = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com/</loc></url>
  <url><loc>https://example.com/about</loc></url>
  <url><loc>https://example.com/contact</loc></url>
</urlset>
"""

LLMS_TXT = "# Characterization Corp\n\n- [Home](https://example.com/)\n"

BLOCKS_HTML = """<!DOCTYPE html>
<html><head><title>Blocks</title></head><body>
<h2>First Heading</h2>
<p>First paragraph containing several words.</p>
<h2>Second Heading</h2>
<p>Second paragraph containing a few more words.</p>
</body></html>"""

CSR_SHELL_HTML = """<!DOCTYPE html>
<html><head><title>Client App</title></head><body>
<div id="app"></div>
<script src="/bundle.js"></script>
</body></html>"""


def _routes(**overrides):
    routes = {
        _BASE_URL: _Response(
            PAGE_HTML,
            headers={"Strict-Transport-Security": "max-age=31536000"},
        ),
        "https://example.com/robots.txt": _Response(ROBOTS_CLOUDFLARE),
        "https://example.com/llms.txt": _Response(LLMS_TXT),
        "https://example.com/sitemap.xml": _Response(SITEMAP_XML),
    }
    routes.update(overrides)
    return routes


def _run_cli(capsys, monkeypatch, routes, *argv):
    def fake_get(url, **_kwargs):
        return routes.get(url, _Response(status_code=404))

    monkeypatch.setattr(requests, "get", fake_get)
    monkeypatch.setattr(sys, "argv", ["fetch_page.py", *argv])
    exit_exc = None
    try:
        runpy.run_path(str(_fetch_page_path()), run_name="__main__")
    except SystemExit as exc:
        exit_exc = exc
    captured = capsys.readouterr()
    return captured, exit_exc


def _cli_json(capsys, monkeypatch, routes, *argv):
    captured, exit_exc = _run_cli(capsys, monkeypatch, routes, *argv)
    assert exit_exc is None or exit_exc.code == 0, (
        f"unexpected exit {exit_exc!r}; stderr={captured.err!r}"
    )
    return json.loads(captured.out)


class TestFetchPageCliModes:
    def test_default_mode_is_page_and_emits_expected_json(self, capsys, monkeypatch):
        data = _cli_json(capsys, monkeypatch, _routes(), _BASE_URL)
        assert data["url"] == _BASE_URL
        assert data["status_code"] == 200
        assert data["title"] == "Characterization Corp — Home"
        assert data["description"] == "A fixed fixture page used for behavior characterization."
        assert data["canonical"] == "https://example.com/"
        assert data["h1_tags"] == ["Characterization Corp"]
        assert data["word_count"] > 0
        assert data["has_ssr_content"] is True
        assert data["errors"] == []
        assert data["structured_data"][0]["@type"] == "Organization"
        assert data["security_headers"]["Strict-Transport-Security"] == "max-age=31536000"

    def test_explicit_page_mode_matches_default(self, capsys, monkeypatch):
        data = _cli_json(capsys, monkeypatch, _routes(), _BASE_URL, "page")
        assert data["title"] == "Characterization Corp — Home"
        assert data["errors"] == []

    def test_page_mode_flags_client_side_shell(self, capsys, monkeypatch):
        routes = _routes(**{_BASE_URL: _Response(CSR_SHELL_HTML)})
        data = _cli_json(capsys, monkeypatch, routes, _BASE_URL, "page")
        assert data["has_ssr_content"] is False
        assert any("client-side" in e.lower() for e in data["errors"])

    def test_page_mode_rejects_unsupported_scheme_without_http(self, capsys, monkeypatch):
        def no_http(url, **_kwargs):
            raise AssertionError("ftp URL must not trigger an HTTP request")

        monkeypatch.setattr(requests, "get", no_http)
        data = _cli_json(capsys, monkeypatch, {}, "ftp://example.com/file", "page")
        assert data["status_code"] is None
        assert any("Unsupported URL scheme" in e for e in data["errors"])

    def test_robots_mode_marks_cloudflare_managed(self, capsys, monkeypatch):
        data = _cli_json(capsys, monkeypatch, _routes(), _BASE_URL, "robots")
        assert data["url"] == "https://example.com/robots.txt"
        assert data["exists"] is True
        assert data["cloudflare_managed"] is True
        assert data["ai_crawler_status"]["GPTBot"] == "BLOCKED"
        assert data["ai_crawler_status"]["ClaudeBot"] == "BLOCKED"
        assert data["sitemaps"] == ["https://example.com/sitemap.xml"]
        assert data["errors"] == []

    def test_robots_mode_plain_is_not_flagged(self, capsys, monkeypatch):
        routes = _routes(**{
            "https://example.com/robots.txt": _Response(ROBOTS_PLAIN),
        })
        data = _cli_json(capsys, monkeypatch, routes, _BASE_URL, "robots")
        assert data["cloudflare_managed"] is False
        assert data["ai_crawler_status"]["GPTBot"] == "ALLOWED_BY_DEFAULT"

    def test_robots_mode_missing_is_not_flagged(self, capsys, monkeypatch):
        routes = _routes(**{
            "https://example.com/robots.txt": _Response(status_code=404),
        })
        data = _cli_json(capsys, monkeypatch, routes, _BASE_URL, "robots")
        assert data["exists"] is False
        assert data["cloudflare_managed"] is False
        assert "No robots.txt found (404)" in data["errors"]
        assert set(data["ai_crawler_status"].values()) == {"NO_ROBOTS_TXT"}

    def test_llms_mode_reports_both_files(self, capsys, monkeypatch):
        data = _cli_json(capsys, monkeypatch, _routes(), _BASE_URL, "llms")
        assert data["llms_txt"]["url"] == "https://example.com/llms.txt"
        assert data["llms_txt"]["exists"] is True
        assert data["llms_txt"]["content"] == LLMS_TXT
        assert data["llms_full_txt"]["url"] == "https://example.com/llms-full.txt"
        assert data["llms_full_txt"]["exists"] is False
        assert data["errors"] == []

    def test_sitemap_mode_returns_pages_and_count(self, capsys, monkeypatch):
        data = _cli_json(capsys, monkeypatch, _routes(), _BASE_URL, "sitemap")
        assert set(data["pages"]) == {
            "https://example.com/",
            "https://example.com/about",
            "https://example.com/contact",
        }
        assert data["count"] == 3

    def test_blocks_mode_returns_heading_sections(self, capsys, monkeypatch):
        routes = _routes(**{_BASE_URL: _Response(BLOCKS_HTML)})
        data = _cli_json(capsys, monkeypatch, routes, _BASE_URL, "blocks")
        assert len(data) == 2
        assert data[1]["heading"] == "Second Heading"
        assert "Second paragraph" in data[1]["content"]
        assert data[1]["word_count"] > 0

    def test_full_mode_combines_all_four_sections(self, capsys, monkeypatch):
        data = _cli_json(capsys, monkeypatch, _routes(), _BASE_URL, "full")
        assert set(data) == {"page", "robots", "llms", "sitemap"}
        assert data["page"]["title"] == "Characterization Corp — Home"
        assert data["robots"]["cloudflare_managed"] is True
        assert data["llms"]["llms_txt"]["exists"] is True
        assert set(data["sitemap"]) == {
            "https://example.com/",
            "https://example.com/about",
            "https://example.com/contact",
        }

    def test_unknown_mode_exits_one_with_literal_message(self, capsys, monkeypatch):
        captured, exit_exc = _run_cli(
            capsys, monkeypatch, _routes(), _BASE_URL, "bogus"
        )
        assert exit_exc is not None and exit_exc.code == 1
        assert captured.out.strip() == "Unknown mode: bogus"

    def test_no_arguments_exits_one_with_usage(self, capsys, monkeypatch):
        captured, exit_exc = _run_cli(capsys, monkeypatch, _routes())
        assert exit_exc is not None and exit_exc.code == 1
        assert "Usage: python fetch_page.py <url> [mode]" in captured.out
        assert "Modes: page (default), robots, llms, sitemap, blocks, full" in captured.out


@pytest.fixture(scope="module")
def webapp():
    path = _webapp_path()
    spec = importlib.util.spec_from_file_location("_geo_char_webapp", path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    module.app.template_folder = str(_TEMPLATES)
    return module


class TestWebappRegionBehavior:
    @pytest.mark.parametrize(
        "prospect,expected",
        [
            ({"region": "CN", "country": "China"}, "CN"),
            ({"country": "Italy"}, "Italy"),
            ({"region": "", "country": "Italy"}, "Italy"),
            ({}, "—"),
        ],
    )
    def test_region_label_return_contract(self, webapp, prospect, expected):
        assert webapp.region_label(prospect) == expected

    def test_jinja_format_region_filter_uses_same_contract(self, webapp):
        assert webapp.app.jinja_env.filters["format_region"]({"country": "Italy"}) == "Italy"
        assert webapp.app.jinja_env.filters["format_region"](
            {"region": "CN", "country": "China"}
        ) == "CN"

    def _client(self, webapp, tmp_path, monkeypatch, prospects):
        crm_path = tmp_path / "prospects.json"
        crm_path.write_text(json.dumps(prospects), encoding="utf-8")
        monkeypatch.setattr(webapp, "CRM_PATH", crm_path)
        monkeypatch.setattr(webapp, "PROPOSALS_DIR", tmp_path / "proposals")
        monkeypatch.setattr(webapp, "AUDITS_DIR", tmp_path / "audits")
        return webapp.app.test_client()

    def test_dashboard_html_shows_region_value(self, webapp, tmp_path, monkeypatch):
        client = self._client(webapp, tmp_path, monkeypatch, [{
            "id": "p1",
            "company": "Example CN",
            "domain": "example.cn",
            "status": "lead",
            "geo_score": 72,
            "region": "CN",
            "country": "China",
        }])
        response = client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Regione" in html
        assert "CN" in html

    def test_dashboard_html_falls_back_to_country(self, webapp, tmp_path, monkeypatch):
        client = self._client(webapp, tmp_path, monkeypatch, [{
            "id": "p2",
            "company": "Example IT",
            "domain": "example.it",
            "status": "active",
            "geo_score": 85,
            "country": "Italy",
        }])
        response = client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Regione" in html
        assert "Italy" in html

    def test_prospect_html_shows_region_and_country_fallback(
        self, webapp, tmp_path, monkeypatch
    ):
        client = self._client(webapp, tmp_path, monkeypatch, [
            {
                "id": "p1",
                "company": "Example CN",
                "domain": "example.cn",
                "status": "lead",
                "geo_score": 72,
                "region": "CN",
                "country": "China",
            },
            {
                "id": "p2",
                "company": "Example IT",
                "domain": "example.it",
                "status": "active",
                "geo_score": 85,
                "country": "Italy",
            },
        ])
        cn_html = client.get("/prospect/p1").get_data(as_text=True)
        it_html = client.get("/prospect/p2").get_data(as_text=True)
        assert "Regione" in cn_html and "CN" in cn_html
        assert "Regione" in it_html and "Italy" in it_html

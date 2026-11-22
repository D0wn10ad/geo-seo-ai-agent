import importlib.util
import json
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "skills" / "geo" / "scripts" / "webapp" / "app.py"


spec = importlib.util.spec_from_file_location("geo_webapp", MODULE_PATH)
geo_webapp = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(geo_webapp)
geo_webapp.app.template_folder = str(MODULE_PATH.parent / "templates")


def write_prospects(path: Path, prospects: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(prospects), encoding="utf-8")


def test_region_label_prefers_region_over_country():
    prospect = {"region": "CN", "country": "China"}

    assert geo_webapp.region_label(prospect) == "CN"


def test_region_label_falls_back_to_country():
    prospect = {"country": "Italy"}

    assert geo_webapp.region_label(prospect) == "Italy"


def test_dashboard_and_prospect_render_region(tmp_path, monkeypatch):
    crm_path = tmp_path / "prospects.json"
    write_prospects(
        crm_path,
        [
            {
                "id": "p1",
                "company": "Example CN",
                "domain": "example.cn",
                "status": "lead",
                "geo_score": 72,
                "region": "CN",
                "country": "China",
            }
        ],
    )

    monkeypatch.setattr(geo_webapp, "CRM_PATH", crm_path)
    monkeypatch.setattr(geo_webapp, "PROPOSALS_DIR", tmp_path / "proposals")
    monkeypatch.setattr(geo_webapp, "AUDITS_DIR", tmp_path / "audits")

    client = geo_webapp.app.test_client()

    dashboard = client.get("/")
    assert dashboard.status_code == 200
    dashboard_html = dashboard.get_data(as_text=True)
    assert "Regione" in dashboard_html
    assert "CN" in dashboard_html

    prospect = client.get("/prospect/p1")
    assert prospect.status_code == 200
    prospect_html = prospect.get_data(as_text=True)
    assert "Regione" in prospect_html
    assert "CN" in prospect_html

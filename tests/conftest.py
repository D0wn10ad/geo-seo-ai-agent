import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "geo" / "scripts"
CHAR_MODULE_FILE = "test_surviving_behavior_characterization.py"


def pytest_configure(config):
    os.environ.setdefault("GEO_CHAR_FETCH_PAGE_PATH", str(SCRIPTS / "fetch_page.py"))
    os.environ.setdefault("GEO_CHAR_WEBAPP_APP_PATH", str(SCRIPTS / "webapp" / "app.py"))


def pytest_collection_modifyitems(config, items):
    for module in list(sys.modules.values()):
        path = getattr(module, "__file__", None)
        if path and Path(path).name == CHAR_MODULE_FILE and hasattr(module, "_TEMPLATES"):
            module._TEMPLATES = SCRIPTS / "webapp" / "templates"

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MOD = ROOT / "action" / "software-system_dev" / "architecture_view.py"


def load_module():
    spec = importlib.util.spec_from_file_location("architecture_view", MOD)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_create_spec_from_software_system_view_without_provider_fields():
    mod = load_module()
    result = mod.create_spec({
        "subject": "Payments",
        "model_view": {
            "schema_version": "SoftwareSystemView/v1",
            "system": {"name": "Payments"},
            "components": [{"id": "api", "name": "API"}, {"id": "db", "name": "DB"}],
            "dependencies": [{"id": "d1", "source": "api", "target": "db"}],
        },
    })
    assert result["exit"] == 0, result
    spec = result["spec"]
    assert spec["schema_version"] == "ArchitectureViewSpec/v1"
    assert spec["view_type"] == "architecture"
    assert spec["subject"] == "Payments"
    assert [c["id"] for c in spec["components"]] == ["api", "db"]
    assert spec["dependencies"][0]["source"] == "api"
    assert "archify" not in spec

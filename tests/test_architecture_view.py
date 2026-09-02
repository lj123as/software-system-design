import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "action" / "software-system_dev" / "architecture_view.py"


def load_module():
    spec = importlib.util.spec_from_file_location("software_system_architecture_view", MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sample_view():
    return {
        "schema_version": "SoftwareSystemView/v1",
        "system": {"id": "ka", "name": "KA Vault"},
        "components": [
            {"id": "ai-workspace", "name": "AI Workspace", "kind": "component"},
            {"id": "aihw", "name": "AIHW", "kind": "component"},
        ],
        "dependencies": [
            {"id": "workspace-aihw", "source": "ai-workspace", "target": "aihw", "type": "uses"},
        ],
    }


def test_create_architecture_view_spec_is_provider_neutral():
    m = load_module()

    result = m.create_spec({"subject": "KA Vault", "model_view": sample_view()})

    assert result["exit"] == 0, result
    spec = result["spec"]
    assert spec["schema_version"] == "ArchitectureViewSpec/v1"
    assert spec["view_type"] == "architecture"
    assert spec["subject"] == "KA Vault"
    assert [c["id"] for c in spec["components"]] == ["ai-workspace", "aihw"]
    assert spec["dependencies"][0]["source"] == "ai-workspace"
    assert "archify" not in json.dumps(spec).lower()


def test_internal_provider_generates_view_model():
    m = load_module()
    spec = m.create_spec({"subject": "KA Vault", "model_view": sample_view()})["spec"]

    result = m.internal_provider(spec)

    assert result["exit"] == 0, result
    model = result["view_model"]
    assert model["schema_version"] == "ViewModel/v1"
    assert model["view_type"] == "architecture"
    assert model["layout"]["type"] == "layered"
    assert model["nodes"][0]["source"] == "software-system_dev"
    assert model["edges"][0]["target"] == "aihw"


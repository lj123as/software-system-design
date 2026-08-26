import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOST_FILE = ROOT / "design_model.py"


def load_design_model():
    spec = importlib.util.spec_from_file_location("software_system_design_model", HOST_FILE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sample_canvas():
    return {
        "canvasId": "canvas-arch",
        "name": "Order System",
        "nodes": [
            {"id": "n-api", "label": "API Service", "kind": "frame"},
            {"id": "n-db", "label": "Order Database", "kind": "frame"},
        ],
        "connectors": [
            {"id": "c-api-db", "source": "n-api", "target": "n-db"},
        ],
    }


def test_schema_declares_ten_skeleton_objects():
    design_model = load_design_model()
    result = design_model.schema()
    assert result["exit"] == 0, result
    names = [obj["name"] for obj in result["objects"]]
    assert names == [
        "System",
        "Component",
        "Module",
        "Interface",
        "DataModel",
        "Runtime",
        "Deployment",
        "Dependency",
        "ADR",
        "ProjectionTarget",
    ]


def test_extract_builds_view_from_canvas_snapshot():
    design_model = load_design_model()
    result = design_model.extract(sample_canvas())
    assert result["exit"] == 0, result
    view = result["view"]
    assert view["schema_version"] == "SoftwareSystemView/v1"
    assert [c["id"] for c in view["components"]] == ["n-api", "n-db"]
    assert view["dependencies"][0]["source"] == "n-api"


def test_recognize_only_when_components_exist():
    design_model = load_design_model()
    recognized = design_model.recognize(sample_canvas())
    assert recognized["exit"] == 0, recognized
    assert recognized["model_view"]["components"]
    empty = design_model.recognize({"canvasId": "empty"})
    assert empty["exit"] == 1


def test_validate_reports_duplicate_and_dangling():
    design_model = load_design_model()
    view = {
        "components": [{"id": "a"}, {"id": "a"}],
        "dependencies": [{"id": "d1", "source": "a", "target": "missing"}],
    }
    result = design_model.validate(view)
    assert result["exit"] == 2, result
    codes = {issue["code"] for issue in result["issues"]}
    assert "DUPLICATE_COMPONENT_ID" in codes
    assert "DEPENDENCY_ENDPOINT_DANGLING" in codes


def test_explain_renders_components_and_dependencies():
    design_model = load_design_model()
    view = design_model.extract(sample_canvas())["view"]
    result = design_model.explain(view)
    assert result["exit"] == 0, result
    assert "API Service" in result["explanation"]
    assert "n-api -> n-db" in result["explanation"]


def test_propose_patch_is_draft_first():
    design_model = load_design_model()
    result = design_model.propose_patch({}, {"intent": "add module"})
    assert result["exit"] == 0, result
    proposal = result["proposal"]
    assert proposal["type"] == "SoftwareSystemProposal/v1"
    assert proposal["status"] == "draft"
    assert proposal["review_status"] == "needs_review"


def test_project_emits_projection_draft():
    design_model = load_design_model()
    view = design_model.extract(sample_canvas())["view"]
    result = design_model.project(view, {"kind": "architecture-doc"})
    assert result["exit"] == 0, result
    assert result["projection"]["type"] == "SoftwareSystemProjectionDraft/v1"
    assert "Order System" in result["projection"]["content"]

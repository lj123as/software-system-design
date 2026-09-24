#!/usr/bin/env python3
"""Architecture ViewSpec owned by software-system-design.

This module selects what to show for an architecture view. It deliberately
does not know Archify-specific IR; providers adapt this neutral spec.
"""

SPEC_VERSION = "ArchitectureViewSpec/v1"
VIEW_MODEL_VERSION = "ViewModel/v1"


def create_spec(payload, vault=None):
    payload = payload or {}
    view = payload.get("model_view") or payload.get("view") or {}
    if view.get("schema_version") != "SoftwareSystemView/v1":
        return {"exit": 2, "error": "ArchitectureViewSpec requires SoftwareSystemView/v1"}
    system = view.get("system") or {}
    subject = payload.get("subject") or system.get("name") or system.get("id") or "software-system"
    components = [
        {
            "id": c.get("id"),
            "label": c.get("name") or c.get("label") or c.get("id"),
            "kind": c.get("kind", "component"),
            "source": c.get("nodeRef") or c.get("id"),
        }
        for c in (view.get("components") or [])
        if isinstance(c, dict) and c.get("id")
    ]
    dependencies = [
        {
            "id": d.get("id") or str(d.get("source")) + "->" + str(d.get("target")),
            "source": d.get("source"),
            "target": d.get("target"),
            "kind": d.get("kind", "dependency"),
        }
        for d in (view.get("dependencies") or [])
        if isinstance(d, dict) and d.get("source") and d.get("target")
    ]
    return {
        "exit": 0,
        "spec": {
            "schema_version": SPEC_VERSION,
            "view_type": "architecture",
            "subject": subject,
            "scope": payload.get("scope") or {"source": "software-system-design"},
            "components": components,
            "dependencies": dependencies,
        },
    }


def internal_architecture_provider(spec, vault=None):
    nodes = []
    layout = {}
    for i, component in enumerate(spec.get("components") or []):
        node_id = component.get("id")
        if not node_id:
            continue
        nodes.append({"id": node_id, "label": component.get("label") or node_id, "kind": component.get("kind", "component")})
        layout[node_id] = {"x": 80 + i * 180, "y": 80}
    edges = [
        {"id": d.get("id") or str(d.get("source")) + "->" + str(d.get("target")), "source": d.get("source"), "target": d.get("target"), "label": d.get("kind", "depends_on")}
        for d in (spec.get("dependencies") or [])
        if d.get("source") and d.get("target")
    ]
    return {"exit": 0, "view_model": {"schema_version": VIEW_MODEL_VERSION, "view_type": "architecture", "nodes": nodes, "edges": edges, "layout": layout, "metadata": {"owner": "software-system-design"}, "source_spec": spec}}

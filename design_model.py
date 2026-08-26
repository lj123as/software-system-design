#!/usr/bin/env python3
"""Software System Design Model provider (v1).

Traditional / general-purpose software system design model owned by
software-system. The Semantic Model Host consumes this provider through
action/software-system/semantic-model.json. This model never writes AIHW
canvas canonical directly; canvas changes go through AIHW element mutation
proposals.
"""

MODEL_VERSION = "SoftwareSystemDesignModel/v1"
VIEW_VERSION = "SoftwareSystemView/v1"
PROPOSAL_VERSION = "SoftwareSystemProposal/v1"
PROJECTION_VERSION = "SoftwareSystemProjectionDraft/v1"

OBJECTS = [
    {"name": "System", "fields": ["id", "name", "version", "boundaries"]},
    {"name": "Component", "fields": ["id", "name", "kind", "dependencies"]},
    {"name": "Module", "fields": ["id", "name", "componentRef", "responsibilities"]},
    {"name": "Interface", "fields": ["id", "name", "direction", "protocol", "contractRef"]},
    {"name": "DataModel", "fields": ["id", "name", "entities", "relations"]},
    {"name": "Runtime", "fields": ["id", "environment", "processModel"]},
    {"name": "Deployment", "fields": ["id", "topology", "environments"]},
    {"name": "Dependency", "fields": ["id", "source", "target", "kind", "versionConstraint"]},
    {"name": "ADR", "fields": ["id", "title", "status", "decision", "context"]},
    {"name": "ProjectionTarget", "fields": ["id", "kind", "format"]},
]


def _nodes(canvas):
    if not isinstance(canvas, dict):
        return []
    nodes = canvas.get("nodes")
    return nodes if isinstance(nodes, list) else []


def _connectors(canvas):
    if not isinstance(canvas, dict):
        return []
    connectors = canvas.get("connectors")
    return connectors if isinstance(connectors, list) else []


def schema(vault=None):
    return {
        "exit": 0,
        "schema_version": MODEL_VERSION,
        "model": "software_system.design_model_provider",
        "objects": OBJECTS,
        "boundaries": [
            "not agentic-software (traditional software system only)",
            "not an AIHW semantic host",
            "canvas writes only via AIHW ElementMutationProposal",
        ],
    }


def extract(canvas, binding=None, vault=None):
    canvas = canvas or {}
    components = [
        {
            "id": node.get("id"),
            "name": node.get("label") or node.get("name") or node.get("id"),
            "kind": node.get("kind", "node"),
            "nodeRef": node.get("id"),
        }
        for node in _nodes(canvas)
        if isinstance(node, dict) and node.get("id")
    ]
    dependencies = [
        {
            "id": connector.get("id"),
            "source": connector.get("source") or connector.get("sourceNodeRef"),
            "target": connector.get("target") or connector.get("targetNodeRef"),
            "kind": "connector",
        }
        for connector in _connectors(canvas)
        if isinstance(connector, dict) and connector.get("id")
    ]
    view = {
        "schema_version": VIEW_VERSION,
        "canvasId": canvas.get("canvasId") or canvas.get("id"),
        "system": {
            "id": canvas.get("canvasId") or canvas.get("id") or "system-1",
            "name": canvas.get("name") or "Untitled System",
            "version": "0.1",
        },
        "components": components,
        "modules": [],
        "interfaces": [],
        "dataModels": [],
        "runtime": None,
        "deployment": None,
        "dependencies": dependencies,
        "adrs": [],
        "projectionTargets": [],
    }
    return {"exit": 0, "view": view, "issues": []}


def recognize(canvas, selection=None, vault=None):
    view = extract(canvas, selection, vault)["view"]
    if not view["components"]:
        return {"exit": 1, "error": "no software system instance found", "model_view": view}
    return {"exit": 0, "model_view": view, "confidence": "low"}


def validate(model_view, context=None, vault=None):
    view = model_view or {}
    issues = []
    seen = {}
    for component in view.get("components") or []:
        component_id = component.get("id")
        if not component_id:
            issues.append({"code": "MISSING_COMPONENT_ID", "message": "component id required"})
        elif component_id in seen:
            issues.append({"code": "DUPLICATE_COMPONENT_ID", "message": "duplicate component id: " + str(component_id)})
        seen[component_id] = True
    component_ids = {cid for cid in seen if cid}
    for dependency in view.get("dependencies") or []:
        source = dependency.get("source")
        target = dependency.get("target")
        if not source or not target:
            issues.append({"code": "DEPENDENCY_ENDPOINT_MISSING", "message": "dependency requires source and target", "dependencyId": dependency.get("id")})
        elif source not in component_ids or target not in component_ids:
            issues.append({"code": "DEPENDENCY_ENDPOINT_DANGLING", "message": "dependency endpoint must reference components", "dependencyId": dependency.get("id")})
    return {"exit": 0 if not issues else 2, "valid": not issues, "issues": issues}


def explain(model_view, context=None, vault=None):
    view = model_view or {}
    system = view.get("system") or {}
    lines = ["# Software System " + str(system.get("name") or system.get("id") or ""), "", "## Components"]
    components = view.get("components") or []
    if components:
        for component in components:
            lines.append("- " + str(component.get("id")) + " (" + str(component.get("kind", "node")) + "): " + str(component.get("name")))
    else:
        lines.append("(none)")
    lines.append("")
    lines.append("## Dependencies")
    dependencies = view.get("dependencies") or []
    if dependencies:
        for dependency in dependencies:
            lines.append("- " + str(dependency.get("source")) + " -> " + str(dependency.get("target")))
    else:
        lines.append("(none)")
    return {"exit": 0, "explanation": "\n".join(lines)}


def propose_patch(model_view, instruction, vault=None):
    proposal = {
        "type": PROPOSAL_VERSION,
        "status": "draft",
        "review_status": "needs_review",
        "source": "software-system.design_model_provider",
        "target": "software-system.design_model",
        "instruction": instruction or {},
        "patches": [],
    }
    return {"exit": 0, "proposal": proposal}


def project(model_view, target=None, vault=None):
    target = target or {"kind": "architecture-doc"}
    view = model_view or {}
    lines = ["# Architecture Projection: " + str((view.get("system") or {}).get("name") or ""), ""]
    for component in view.get("components") or []:
        lines.append("- " + str(component.get("name")))
    projection = {
        "type": PROJECTION_VERSION,
        "target": target,
        "status": "draft",
        "review_status": "needs_review",
        "content": "\n".join(lines),
    }
    return {"exit": 0, "projection": projection}

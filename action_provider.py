#!/usr/bin/env python3
"""Software System action provider (v1): runtime face of the Type Capability component.

create/update/execute/validate are invoked by K-Action_orchestrator action_ops.py
for action_type=software-system. Design-model face stays in design_model.py
(schema / recognize / extract / validate / explain / propose_patch / project).
Stdlib only.
"""
from datetime import datetime, timezone


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def create_instance(spec, vault=None):
    """Materialize an approved ActionSpecification into a SoftwareSystemInstance skeleton."""
    spec = spec or {}
    atype = str(spec.get("action_type", "")).strip()
    if atype != "software-system":
        return {"exit": 2, "error": "create_instance only supports action_type=software-system; got: " + atype}
    subject = str(spec.get("subject", ""))
    instance = {
        "instance_type": "SoftwareSystemInstance/v1",
        "spec_id": str(spec.get("spec_id", "")),
        "action_type": atype,
        "intent": str(spec.get("intent", "create")),
        "subject": subject,
        "provider": "software-system_dev",
        "state": "created",
        "system": {"id": "sys-" + (subject or "untitled"), "name": subject or "untitled",
                   "version": "0.1.0", "boundaries": [], "status": "created"},
        "components": [],
        "input": spec.get("input") or {},
        "created_at": _now(),
    }
    return {"exit": 0, "instance": instance}


def update_instance(instance, request, vault=None):
    instance = instance or {}
    request = request or {}
    for k in ("intent", "subject", "input"):
        if request.get(k):
            instance[k] = request[k]
    instance["state"] = "updated"
    instance["updated_at"] = _now()
    return {"exit": 0, "instance": instance}


def execute(instance, request, vault=None):
    """Software-system execute: reserved domain behavior; design-model operations
    (propose_patch / project) are the future projection path. Currently reports done."""
    instance = instance or {}
    subject = str(instance.get("subject") or (request or {}).get("subject") or "")
    return {"exit": 0, "state": "done", "executed": True,
            "note": "software-system execute stub (subject=" + subject + ")"}


def validate(instance, request, vault=None):
    instance = instance or {}
    issues = []
    if not instance.get("instance_id"):
        issues.append("missing instance_id")
    if instance.get("action_type") != "software-system":
        issues.append("action_type mismatch")
    if issues:
        return {"exit": 2, "valid": False, "issues": issues}
    return {"exit": 0, "valid": True}

# -*- coding: utf-8 -*-
import importlib.util
from pathlib import Path


AP = Path(__file__).resolve().parents[1] / "action_provider.py"


def load_provider():
    spec = importlib.util.spec_from_file_location("sw_action_provider", AP)
    m = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(m)
    return m


def test_create_gate_and_skeleton():
    prov = load_provider()
    assert prov.create_instance({"action_type": "agentic-software"})["exit"] == 2
    ok = prov.create_instance({"action_type": "software-system", "spec_id": "s1", "subject": "stock"})
    assert ok["exit"] == 0
    inst = ok["instance"]
    assert inst["system"]["id"] == "sys-stock"
    assert inst["provider"] == "software-system_dev"


def test_update_validate_execute():
    prov = load_provider()
    inst = {"instance_id": "act-1", "action_type": "software-system", "subject": "stock", "state": "created"}
    assert prov.update_instance(inst, {"intent": "run"})["instance"]["intent"] == "run"
    assert prov.validate({"instance_id": "act-1", "action_type": "software-system"}, {})["valid"] is True
    assert prov.validate({"action_type": "x"}, {})["valid"] is False
    ex = prov.execute({"subject": "stock"}, {})
    assert ex["state"] == "done" and ex["executed"] is True

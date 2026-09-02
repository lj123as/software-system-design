# Software System Architecture View Provider Chain Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make software-system_dev produce provider-neutral ArchitectureViewSpec/v1 and ViewModel/v1 for AIHW materialization.

**Architecture:** software-system_dev owns architecture view semantics. AI Workspace passes SoftwareSystemView/v1 input, software-system_dev creates ArchitectureViewSpec/v1, and providers convert it to ViewModel/v1 without Archify-specific fields in the spec.

**Tech Stack:** Python view-domain contract, pytest, internal provider; Archify remains an external preview provider until the internal chain passes.

---

## Scope

- Keep ArchitectureViewSpec provider-neutral and owned by software-system_dev.
- Use internal provider for P0/P1 real-chain acceptance.
- Only connect Archify after canonical AIHW writing and rendering are reliable.
- Do not make AI Workspace the owner of architecture view semantics.

## Acceptance Tests

- view_spec_create domain=software-system_dev returns ArchitectureViewSpec/v1 with no archify field.
- internal provider returns ViewModel/v1 nodes and edges matching components/dependencies.
- python -m pytest action/software-system_dev/tests/ -q passes.

## Status Update — 2026-09-02

- Done: software-system_dev remains the owner of provider-neutral ArchitectureViewSpec/v1.
- Done: archify is now an external provider option for the architecture view domain and returns normalized ViewModel/v1 for AIHW materialization.
- Kept boundary: Archify-specific IR is generated inside action/archify; it is not added to ArchitectureViewSpec/v1.
- Next: add richer SoftwareSystemView extraction only when real component/dependency facts are available.

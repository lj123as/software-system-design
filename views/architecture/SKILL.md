# Architecture View Projection

Guidance for producing an `ArchitectureViewSpec/v1` candidate from a Software System Model.
This file is the View Definition's agent guidance; `definition.yaml` is its machine contract.

## Pick the smallest view that makes the point clear

Include only what answers the current question:

- major components and their boundaries
- dependencies between them
- external systems the question actually touches

Ignore, unless the question is about them:

- implementation detail inside a component
- internal modules of a component the reader is not asking about
- deployment topology, data models, and runtime detail

If the reader asks "how does login work", the architecture view should not grow to cover
everything the system does.

## Output

Produce a candidate ViewSpec, then submit it:

    view_spec_create(view_definition_id="software-system-design/architecture/default", spec={...})

Required shape: `schema_version: ArchitectureViewSpec/v1`, `view_type: architecture`,
`subject`, `components[]` (`id`, `label`, `kind`), `dependencies[]` (`source`, `target`, `kind`).

## Rules

- Project from the Software System Model. Do not invent components the model does not have.
- Do not choose a rendering or layout; that is the View Provider's job.
- Validation belongs to the View Definition's schema; `view_spec_create` rejects a spec that breaks it.


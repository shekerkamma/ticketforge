# Spec Inputs

Accepted `printing-press` input forms:

- API or product name:
  - `printing-press Notion`
- explicit Codex mode:
  - `printing-press Discord codex`
  - `printing-press --spec ./openapi.yaml codex`
- local spec file:
  - `printing-press --spec ./openapi.yaml`
- HAR capture:
  - `printing-press --har ./capture.har --name MyAPI`
- URL:
  - `printing-press https://postman.com/explore`

## Good defaults

- Prefer a local verified spec file when one exists.
- Use HAR when the API surface is discovered from real traffic rather than formal docs.
- Use a docs URL or product URL when discovery has to start from the public surface.

## Internal YAML spec

If there is no OpenAPI spec, `printing-press` can work from an internal YAML description of:

- API metadata
- auth scheme
- resources
- endpoints
- params
- response types

Preserve the wire-level field names from the upstream API instead of renaming them for cosmetics.

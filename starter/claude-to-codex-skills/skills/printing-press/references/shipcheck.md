# Shipcheck

Structural success is not enough.

## Required checks

- build succeeds
- verification commands succeed
- behavior is tested against real or realistic targets
- headline commands and help output are plausible
- failure paths are exercised, not assumed

## Do not call it shipped if only these passed

- `go build`
- schema generation
- static verification

Those are necessary but not sufficient.

## Publish standard

A generated CLI is only ship-ready when it has passed both:

1. structural checks
2. behavioral testing / dogfooding

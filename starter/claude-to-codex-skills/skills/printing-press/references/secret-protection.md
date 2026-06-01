# Secret Protection

Read this before archiving, publishing, or sharing any `printing-press` output.

## Hard rules

- Never store API key values, token values, passwords, or session cookies in repo artifacts.
- Env var names and placeholders are safe; secret values are not.
- Strip auth-bearing headers, cookies, query params, and response bodies from HAR captures before keeping them.

## Practical checks

- run fixed-string scans for exact known secret values before archiving
- redact any discovered exact-value leaks
- remove request/response cookies and auth headers from HAR files
- avoid publishing real workspace or customer PII in proofs or README examples

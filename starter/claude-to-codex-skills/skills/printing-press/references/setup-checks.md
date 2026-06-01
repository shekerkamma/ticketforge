# Setup Checks

Use this before any `printing-press` run.

## Binary check

```bash
command -v printing-press
```

If missing, stop and tell the user to install it:

```bash
go install github.com/mvanhorn/cli-printing-press/v4/cmd/printing-press@latest
```

Then verify:

```bash
printing-press --version
```

## Upgrade check

If the binary exists, it is reasonable to inspect:

```bash
printing-press version --json
```

If the user wants to upgrade, use the same `go install ...@latest` command.

## Compatibility rule

If the installed binary is clearly older than the workflow expects, warn and continue only if the user accepts the risk.

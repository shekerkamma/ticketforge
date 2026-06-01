# Codex GitHub Starter

This starter packages the reusable setup for a GitHub-first Codex workflow.

It is the reusable layer, not the app-specific layer.

Included:

- GitHub issue templates
- GitHub PR template
- Codex master/task prompts
- a generic devcontainer for Codespaces or devcontainer hosts
- a GitHub foundation check script
- a GitHub label bootstrap script
- a Codex CLI install script for cloud/container work
- a generic remote setup doc

Not included:

- app-specific CI
- app-specific backend/frontend bootstrap
- app-specific test or run commands
- app-specific deployment setup

## Apply to another repo

```bash
./starter/codex-github-starter/apply.sh /path/to/repo owner/repo
```

Optional:

```bash
./starter/codex-github-starter/apply.sh /path/to/repo owner/repo --force
```

That writes the reusable Codex/GitHub scaffolding into the target repo.

## After applying

In the target repo:

```bash
./scripts/check_github_foundation.sh
```

If `gh` is authenticated:

```bash
./scripts/bootstrap_github_repo.sh
```

If the repo uses Codespaces or a devcontainer host, rebuild the container after applying the starter so the new devcontainer and Codex CLI install path take effect.

# Contributing to TicketForge

Thanks for your interest in contributing. TicketForge is an open-source multi-agent pipeline that turns GitHub Issues into reviewed pull requests. Contributions are welcome across the agent pipeline, review criteria, test coverage, and documentation.

## Getting Started

```bash
# Clone the repo
git clone https://github.com/shekerkamma/ticketforge.git
cd ticketforge

# Start infrastructure
docker-compose up -d postgres redis

# Backend
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## What to Contribute

### High-impact areas

- **Agent definitions** — New agents or improvements to existing ones in `backend/app/agents/`. Each agent extends `BaseAgent` and implements a `run(context)` method.
- **Review criteria** — Add new review dimensions to the code reviewer in `backend/app/agents/code_reviewer.py`. Current dimensions: style, tests, regression, security.
- **Fix pattern coverage** — Test the pipeline against specific bug categories (null checks, off-by-one, config mismatches) and report accuracy.
- **Test coverage** — Tests live in `backend/tests/`. Both unit tests (mocked services) and integration tests (real DB) are valuable.

### Good first issues

Look for issues labeled `good first issue` in the GitHub Issues tracker. These are scoped to a single file and have clear acceptance criteria.

## Development Workflow

1. Fork the repo and create a feature branch from `main`
2. Make your changes with tests
3. Run the checks:
   ```bash
   cd backend
   ruff check .          # lint
   mypy app/             # type check
   pytest -q             # tests
   ```
4. Open a PR against `main` with a clear description

## Code Style

- **Backend**: Python 3.11+, formatted with ruff, type hints on public APIs
- **Frontend**: TypeScript, Tailwind CSS, Next.js App Router conventions
- **Commits**: Imperative mood, concise subject line ("Add retry logic to code reviewer", not "Added retry logic")

## Agent Architecture

All agents follow the same pattern:

```python
class MyAgent(BaseAgent):
    name = "my_agent"

    async def run(self, context: dict) -> AgentResult:
        await self.log_action("start", {"key": "value"})
        # ... do work ...
        await self.log_observation("what happened")
        await self.log_decision("what was decided", confidence=0.8)
        return AgentResult(success=True, output={...}, confidence=0.8)
```

Key rules:
- Log every significant action, observation, and decision via `self.log_*` methods
- Return `AgentResult` with `success`, `output`, `confidence`, and `tokens_used`
- When confidence is low, return `success=False` to trigger escalation
- Never access production systems — all code execution happens in Docker sandboxes

## Docker Sandbox Safety

The sandbox runs with `--network=none`, 2GB memory limit, and 1 CPU. These constraints are non-negotiable. If you're modifying `DockerService`, do not:
- Enable network access in containers
- Increase memory limits beyond 2GB
- Mount host filesystem paths
- Run containers as root with host capabilities

## Reporting Issues

When filing a bug report, include:
- Steps to reproduce
- Expected vs actual behavior
- Relevant log output (from the event stream if possible)
- Repository size and language (affects sandbox performance)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

import { AuthButtons } from "@/components/marketing/AuthButtons";

const FEATURES = [
  {
    title: "Instant Analysis",
    description:
      "AI agents analyze every bug ticket, identify affected files, and determine the fix strategy in seconds.",
  },
  {
    title: "Autonomous Code Generation",
    description:
      "Sandboxed agents write, test, and iterate on fixes in isolated Docker containers. No access to your prod infra.",
  },
  {
    title: "Human-in-the-Loop Review",
    description:
      "Every fix goes through AI code review before a PR is created. Low-confidence fixes are escalated, never force-merged.",
  },
];

const STEPS = [
  { step: "1", label: "Label an issue", detail: "Add your trigger label (e.g. 'bug') to any GitHub issue." },
  { step: "2", label: "AI analyzes", detail: "Content Researcher agent extracts problem scope and affected files." },
  { step: "3", label: "Code generated", detail: "CodeAct agent writes and tests a fix in a sandboxed container." },
  { step: "4", label: "PR created", detail: "After code review passes, a PR appears on your repo. You just merge." },
];

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-surface">
      {/* Hero */}
      <section className="flex flex-col items-center px-6 pb-16 pt-24 text-center">
        <h1 className="max-w-2xl text-4xl font-bold tracking-tight text-on-surface sm:text-5xl">
          Your routine bugs fix themselves.
        </h1>
        <p className="mt-4 max-w-lg text-lg text-on-surface-muted">
          TicketForge turns GitHub issues into merged pull requests using a
          multi-agent AI pipeline. Label a bug, get a PR.
        </p>
        <AuthButtons />
        <p className="mt-3 text-xs text-on-surface-muted">
          Free tier: 20 tickets/month. No credit card required.
        </p>
      </section>

      {/* Features */}
      <section className="border-t border-border bg-surface-raised px-6 py-16">
        <div className="mx-auto max-w-4xl">
          <h2 className="mb-8 text-center text-2xl font-semibold text-on-surface">
            Why teams use TicketForge
          </h2>
          <div className="grid gap-6 sm:grid-cols-3">
            {FEATURES.map((f) => (
              <div
                key={f.title}
                className="rounded-lg border border-border bg-surface p-6"
              >
                <h3 className="text-sm font-semibold text-on-surface">
                  {f.title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-on-surface-muted">
                  {f.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="px-6 py-16">
        <div className="mx-auto max-w-3xl">
          <h2 className="mb-8 text-center text-2xl font-semibold text-on-surface">
            How it works
          </h2>
          <div className="space-y-4">
            {STEPS.map((s) => (
              <div
                key={s.step}
                className="flex gap-4 rounded-lg border border-border bg-surface-raised p-4"
              >
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary text-sm font-bold text-white">
                  {s.step}
                </div>
                <div>
                  <p className="text-sm font-semibold text-on-surface">
                    {s.label}
                  </p>
                  <p className="mt-1 text-sm text-on-surface-muted">
                    {s.detail}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border px-6 py-8 text-center text-xs text-on-surface-muted">
        TicketForge &mdash; From ticket to PR. Automatically.
      </footer>
    </main>
  );
}

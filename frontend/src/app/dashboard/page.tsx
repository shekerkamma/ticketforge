"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";
import { createEventStream, type SSEEvent } from "@/lib/sse";
import StatusCards from "@/components/features/StatusCards";
import ActivityFeed from "@/components/features/ActivityFeed";

interface TicketSummary {
  status: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const [counts, setCounts] = useState<Record<string, number>>({});
  const [events, setEvents] = useState<SSEEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [teamId, setTeamId] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      // Get teams first
      const teamsRes = await apiFetch("/api/v1/teams");
      const teamsData = await teamsRes.json();
      const teams = teamsData.teams || [];

      if (teams.length === 0) {
        setTeamId(null);
        setEvents([]);
        setLoading(false);
        return;
      }

      const currentTeamId = teams[0].id;
      setTeamId(currentTeamId);

      // Get tickets to compute status counts
      const ticketsRes = await apiFetch(
        `/api/v1/teams/${currentTeamId}/tickets?limit=100`
      );
      const ticketsData = await ticketsRes.json();
      const tickets: TicketSummary[] = ticketsData.tickets || [];

      const statusCounts: Record<string, number> = {};
      tickets.forEach((t) => {
        statusCounts[t.status] = (statusCounts[t.status] || 0) + 1;
      });
      setCounts(statusCounts);

      setError(null);
    } catch (e) {
      setError("Failed to load dashboard data. Retrying...");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, [fetchData]);

  useEffect(() => {
    if (!teamId) return;
    return createEventStream(teamId, (event) => {
      setEvents((prev) => {
        const next = [event, ...prev.filter((entry) => entry.id !== event.id)];
        return next.slice(0, 10);
      });
    });
  }, [teamId]);

  if (loading) {
    return (
      <div>
        <h1 className="mb-4 text-xl font-semibold text-on-surface">Dashboard</h1>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-7">
          {Array.from({ length: 7 }).map((_, i) => (
            <div
              key={i}
              className="h-20 animate-pulse rounded-lg border border-border bg-surface-raised"
            />
          ))}
        </div>
      </div>
    );
  }

  if (!teamId) {
    return (
      <div>
        <h1 className="mb-4 text-xl font-semibold text-on-surface">Dashboard</h1>
        <div className="rounded-lg border border-border bg-surface-raised p-8 text-center">
          <p className="mb-4 text-on-surface-muted">
            No repositories connected yet. Connect your first repo to get started.
          </p>
          <button
            onClick={() => router.push("/dashboard/settings")}
            className="inline-flex h-9 items-center rounded-md bg-primary px-4 text-sm font-medium text-white transition-colors hover:bg-primary-hover"
          >
            Connect Repository
          </button>
        </div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="mb-4 text-xl font-semibold text-on-surface">Dashboard</h1>

      {error && (
        <div className="mb-4 rounded-md bg-error-subtle px-4 py-3 text-sm text-error">
          {error}
        </div>
      )}

      <StatusCards
        counts={counts}
        onFilterByStatus={(status) =>
          router.push(`/dashboard/tickets?status=${status}`)
        }
      />

      <div className="mt-6">
        <h2 className="mb-3 text-sm font-semibold text-on-surface">Recent Activity</h2>
        <ActivityFeed events={events} />
      </div>
    </div>
  );
}

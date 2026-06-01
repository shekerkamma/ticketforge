"use client";

import Image from "next/image";
import { useState } from "react";

import { apiFetch } from "@/lib/api";

interface Member {
  github_login: string;
  avatar_url: string | null;
  role: string;
  user_id?: string;
}

interface TeamTabProps {
  teamId: string;
  members: Member[];
  currentUserRole: string;
  onMembersChanged: () => void;
}

export default function TeamTab({
  teamId,
  members,
  currentUserRole,
  onMembersChanged,
}: TeamTabProps) {
  const [inviteUsername, setInviteUsername] = useState("");
  const [inviting, setInviting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const isAdmin = currentUserRole === "owner" || currentUserRole === "admin";

  async function handleInvite(e: React.FormEvent) {
    e.preventDefault();
    if (!inviteUsername.trim()) return;
    setInviting(true);
    setError(null);

    try {
      const res = await apiFetch(`/api/v1/teams/${teamId}/members`, {
        method: "POST",
        body: JSON.stringify({ github_username: inviteUsername.trim() }),
      });
      if (!res.ok) {
        const data = await res.json();
        setError(data.message || data.detail || "Failed to add member");
      } else {
        setInviteUsername("");
        onMembersChanged();
      }
    } catch {
      setError("Failed to add member");
    } finally {
      setInviting(false);
    }
  }

  async function handleRemove(username: string) {
    const member = members.find((m) => m.github_login === username);
    if (!member?.user_id) return;

    try {
      await apiFetch(`/api/v1/teams/${teamId}/members/${member.user_id}`, {
        method: "DELETE",
      });
      onMembersChanged();
    } catch {
      // silently handle
    }
  }

  async function handleRoleChange(username: string, newRole: string) {
    const member = members.find((m) => m.github_login === username);
    if (!member?.user_id) return;

    try {
      await apiFetch(`/api/v1/teams/${teamId}/members/${member.user_id}`, {
        method: "PATCH",
        body: JSON.stringify({ role: newRole }),
      });
      onMembersChanged();
    } catch {
      // silently handle
    }
  }

  return (
    <div>
      <h2 className="mb-3 text-sm font-semibold text-on-surface">
        Team Members
      </h2>

      <div className="rounded-lg border border-border bg-surface-raised">
        {members.map((member) => (
          <div
            key={member.github_login}
            className="flex items-center justify-between border-b border-border px-4 py-3 last:border-b-0"
          >
            <div className="flex items-center gap-3">
              {member.avatar_url && (
                <Image
                  src={member.avatar_url}
                  alt={member.github_login}
                  width={32}
                  height={32}
                  className="h-8 w-8 rounded-full"
                />
              )}
              <div>
                <p className="text-sm font-medium text-on-surface">
                  {member.github_login}
                </p>
                <p className="text-xs capitalize text-on-surface-muted">
                  {member.role}
                </p>
              </div>
            </div>

            {isAdmin && member.role !== "owner" && (
              <div className="flex items-center gap-2">
                <select
                  value={member.role}
                  onChange={(e) =>
                    handleRoleChange(member.github_login, e.target.value)
                  }
                  className="rounded border border-border bg-surface px-2 py-1 text-xs text-on-surface"
                  aria-label={`Role for ${member.github_login}`}
                >
                  <option value="member">Member</option>
                  <option value="admin">Admin</option>
                </select>
                <button
                  onClick={() => handleRemove(member.github_login)}
                  className="rounded px-2 py-1 text-xs text-error hover:bg-error-subtle"
                  aria-label={`Remove ${member.github_login}`}
                >
                  Remove
                </button>
              </div>
            )}
          </div>
        ))}
      </div>

      {isAdmin && (
        <form onSubmit={handleInvite} className="mt-4 flex gap-2">
          <input
            type="text"
            value={inviteUsername}
            onChange={(e) => setInviteUsername(e.target.value)}
            placeholder="GitHub username"
            className="flex-1 rounded-md border border-border bg-surface px-3 py-2 text-sm text-on-surface placeholder:text-on-surface-muted"
          />
          <button
            type="submit"
            disabled={inviting || !inviteUsername.trim()}
            className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary-hover disabled:opacity-50"
          >
            {inviting ? "Adding..." : "Add Member"}
          </button>
        </form>
      )}

      {error && (
        <p className="mt-2 text-sm text-error">{error}</p>
      )}
    </div>
  );
}

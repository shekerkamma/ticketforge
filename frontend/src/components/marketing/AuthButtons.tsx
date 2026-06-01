"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const SHOW_DEV_LOGIN = !process.env.NEXT_PUBLIC_API_URL;

function buildAuthUrl(path: string): string {
  const url = new URL(path, API_URL);
  if (typeof window !== "undefined") {
    url.searchParams.set("return_to", window.location.origin);
  }
  return url.toString();
}

export function AuthButtons() {
  const [githubHref, setGithubHref] = useState(`${API_URL}/api/auth/github`);
  const [devHref, setDevHref] = useState(`${API_URL}/api/auth/dev-login`);

  useEffect(() => {
    setGithubHref(buildAuthUrl("/api/auth/github"));
    setDevHref(buildAuthUrl("/api/auth/dev-login"));
  }, []);

  return (
    <>
      <a
        href={githubHref}
        className="mt-8 inline-flex h-11 items-center rounded-md bg-primary px-6 text-sm font-medium text-white transition-colors hover:bg-primary-hover"
      >
        Sign in with GitHub
      </a>
      {SHOW_DEV_LOGIN && (
        <a
          href={devHref}
          className="mt-3 inline-flex h-9 items-center rounded-md border border-border bg-surface-raised px-4 text-xs font-medium text-on-surface-muted transition-colors hover:bg-surface"
        >
          Dev Login (skip OAuth)
        </a>
      )}
    </>
  );
}

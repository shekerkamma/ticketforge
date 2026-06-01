"use client";

import { Suspense, useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";

function AuthCallbackContent() {
  const searchParams = useSearchParams();
  const router = useRouter();

  useEffect(() => {
    const token = searchParams.get("token");
    if (token) {
      localStorage.setItem("ticketforge_token", token);
      router.replace("/dashboard");
    } else {
      router.replace("/");
    }
  }, [searchParams, router]);

  return (
    <main className="flex min-h-screen items-center justify-center">
      <p className="text-on-surface-muted">Authenticating...</p>
    </main>
  );
}

export default function AuthCallback() {
  return (
    <Suspense
      fallback={
        <main className="flex min-h-screen items-center justify-center">
          <p className="text-on-surface-muted">Authenticating...</p>
        </main>
      }
    >
      <AuthCallbackContent />
    </Suspense>
  );
}

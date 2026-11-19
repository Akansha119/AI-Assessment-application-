"use client";

export const dynamic = "force-dynamic";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { apiFetch, removeAccessToken } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function DashboardPage() {
  const [user, setUser] = useState<{ email: string; display_alias?: string } | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const token = typeof window !== "undefined" ? localStorage.getItem("assessiq_access_token") : null;
    if (!token) {
      router.push("/login");
      return;
    }
    (async () => {
      try {
        const data = await apiFetch<{ email: string; display_alias?: string; id: string; is_active: boolean; created_at: string }>(
          "/api/v1/auth/me",
          { headers: { Authorization: `Bearer ${token}` } }
        );
        setUser(data);
      } catch {
        removeAccessToken();
        router.push("/login");
      } finally {
        setLoading(false);
      }
    })();
  }, [router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <span className="loading">Loading…</span>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold">Dashboard</h1>
            <p className="text-muted-foreground">AssessIQ — competitive examination preparation</p>
          </div>
          <Button onClick={() => { removeAccessToken(); router.push("/login"); router.refresh(); }}>
            Sign out
          </Button>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Welcome, {user.display_alias || user.email}</CardTitle>
            <CardDescription>Your preparation hub.</CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card className="border-none bg-muted p-4">
              <CardTitle className="text-sm">Examinations</CardTitle>
              <CardDescription>Select an exam to begin.</CardDescription>
            </Card>
            <Card className="border-none bg-muted p-4">
              <CardTitle className="text-sm">Tests</CardTitle>
              <CardDescription>Attempt mock and topic-wise tests.</CardDescription>
            </Card>
            <Card className="border-none bg-muted p-4">
              <CardTitle className="text-sm">Analytics</CardTitle>
              <CardDescription>Track your performance trends.</CardDescription>
            </Card>
            <Card className="border-none bg-muted p-4">
              <CardTitle className="text-sm">AI Tutor</CardTitle>
              <CardDescription>Personalized assessment guidance.</CardDescription>
            </Card>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch, getAccessToken } from "@/lib/api";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

export default function AdminDashboardPage() {
  const [stats, setStats] = useState<{
    exams: number;
    subjects: number;
    topics: number;
    users: number;
  }>({ exams: 0, subjects: 0, topics: 0, users: 0 });
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const token = getAccessToken();
    if (!token) {
      router.push("/login");
      return;
    }
    (async () => {
      try {
        const [exams, subjects, topics] = await Promise.all([
          apiFetch<any[]>("/api/v1/exams", {
            headers: { Authorization: `Bearer ${token}` },
          }),
          apiFetch<any[]>("/api/v1/subjects", {
            headers: { Authorization: `Bearer ${token}` },
          }),
          apiFetch<any[]>("/api/v1/topics?subject_id=00000000-0000-0000-0000-000000000000", {
            headers: { Authorization: `Bearer ${token}` },
          }).catch(() => []),
        ]);
        setStats({
          exams: exams.length,
          subjects: subjects.length,
          topics: topics.length,
          users: 0,
        });
      } catch {
        // ignore errors, show zeros
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

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Admin Dashboard</h1>
        <p className="text-muted-foreground">Manage examinations and system configuration.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Examinations" value={stats.exams} icon="📝" />
        <StatCard title="Subjects" value={stats.subjects} icon="📚" />
        <StatCard title="Topics" value={stats.topics} icon="🌳" />
        <StatCard title="Users" value={stats.users} icon="👥" />
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>Get started with examination management.</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-3">
          <QuickAction href="/admin/exams" label="Manage Examinations" icon="📝" />
          <QuickAction href="/admin/subjects" label="Manage Subjects" icon="📚" />
          <QuickAction href="/admin/topics" label="Manage Topics" icon="🌳" />
        </CardContent>
      </Card>
    </div>
  );
}

function StatCard({ title, value, icon }: { title: string; value: number; icon: string }) {
  return (
    <Card className="border-none bg-muted p-4">
      <CardContent className="flex flex-col items-center justify-center text-center py-6">
        <span className="text-2xl mb-2">{icon}</span>
        <div className="text-3xl font-bold">{value}</div>
        <CardTitle className="text-sm">{title}</CardTitle>
      </CardContent>
    </Card>
  );
}

function QuickAction({ href, label, icon }: { href: string; label: string; icon: string }) {
  return (
    <a
      href={href}
      className="flex flex-col items-center justify-center gap-2 p-4 rounded-xl border border-input hover:bg-accent transition-colors text-muted-foreground hover:text-primary"
    >
      <span className="text-2xl">{icon}</span>
      <span className="text-sm font-medium">{label}</span>
    </a>
  );
}

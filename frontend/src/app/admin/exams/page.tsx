"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import {
  createExam,
  deleteExam,
  listExams,
  type Exam,
} from "@/lib/exams";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function ExamsPage() {
  const [exams, setExams] = useState<Exam[]>([]);
  const [loading, setLoading] = useState(false);
  const [creating, setCreating] = useState(false);
  const [code, setCode] = useState("");
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const data = await listExams();
      setExams(data);
    } catch (err: any) {
      setError(err?.message || "Failed to load exams");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setCreating(true);
    try {
      await createExam({ code, name, description: description || undefined });
      setCode("");
      setName("");
      setDescription("");
      await load();
    } catch (err: any) {
      setError(err?.message || "Failed to create exam");
    } finally {
      setCreating(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm("Are you sure you want to delete this examination?")) return;
    try {
      await deleteExam(id);
      await load();
    } catch (err: any) {
      setError(err?.message || "Failed to delete exam");
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Examinations</h1>
          <p className="text-muted-foreground">
            Manage competitive examinations available on AssessIQ.
          </p>
        </div>
        <a href="/admin/exams/new" className="text-sm text-muted-foreground underline underline-offset-4">
          Create Examination
        </a>
      </div>

      {error && (
        <div className="rounded-lg border border-destructive/50 bg-destructive p-3 text-sm text-destructive">
          {error}
        </div>
      )}

      <Card>
        <CardHeader>
          <CardTitle>All Examinations</CardTitle>
          <CardDescription>List of registered examinations.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-input text-left text-muted-foreground">
                  <th className="pb-3 font-medium">Code</th>
                  <th className="pb-3 font-medium">Name</th>
                  <th className="pb-3 font-medium">Description</th>
                  <th className="pb-3 font-medium">Status</th>
                  <th className="pb-3 font-medium text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td colSpan={5} className="p-4 text-center">
                      Loading…
                    </td>
                  </tr>
                ) : exams.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="p-4 text-center text-muted-foreground">
                      No examinations found.
                    </td>
                  </tr>
                ) : (
                  exams.map((exam) => (
                    <tr key={exam.id} className="border-b border-input">
                      <td className="p-3 font-mono text-sm">{exam.code}</td>
                      <td className="p-3">{exam.name}</td>
                      <td className="p-3 text-muted-foreground">
                        {exam.description || "—"}
                      </td>
                      <td className="p-3">
                        <Badge variant={exam.is_active ? "default" : "secondary"}>
                          {exam.is_active ? "Active" : "Inactive"}
                        </Badge>
                      </td>
                      <td className="p-3 text-right">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleDelete(exam.id)}
                        >
                          Delete
                        </Button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Create Examination</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleCreate} className="grid gap-4 md:grid-cols-3">
            <div className="space-y-2">
              <Label htmlFor="exam-code">Exam Code</Label>
              <Input
                id="exam-code"
                placeholder="e.g. DSSSB"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="exam-name">Examination Name</Label>
              <Input
                id="exam-name"
                placeholder="e.g. Delhi Subordinate Services Selection Board"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2 md:col-span-3">
              <Label htmlFor="exam-description">Description</Label>
              <Input
                id="exam-description"
                placeholder="Optional description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>
            <Button type="submit" className="w-auto" disabled={creating}>
              {creating ? "Creating…" : "Create Examination"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

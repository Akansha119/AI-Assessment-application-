"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import {
  createSubject,
  listSubjects,
  type Subject,
} from "@/lib/exams";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function SubjectsPage() {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [loading, setLoading] = useState(false);
  const [creating, setCreating] = useState(false);
  const [code, setCode] = useState("");
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const data = await listSubjects();
      setSubjects(data);
    } catch (err: any) {
      setError(err?.message || "Failed to load subjects");
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
      await createSubject({ code, name, description: description || undefined });
      setCode("");
      setName("");
      setDescription("");
      await load();
    } catch (err: any) {
      setError(err?.message || "Failed to create subject");
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Subjects</h1>
          <p className="text-muted-foreground">
            Manage subjects across examinations.
          </p>
        </div>
      </div>

      {error && (
        <div className="rounded-lg border border-destructive/50 bg-destructive p-3 text-sm text-destructive">
          {error}
        </div>
      )}

      <Card>
        <CardHeader>
          <CardTitle>All Subjects</CardTitle>
          <CardDescription>List of registered subjects.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-input text-left text-muted-foreground">
                  <th className="pb-3 font-medium">Code</th>
                  <th className="pb-3 font-medium">Name</th>
                  <th className="pb-3 font-medium">Description</th>
                  <th className="pb-3 font-medium text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td colSpan={4} className="p-4 text-center">
                      Loading…
                    </td>
                  </tr>
                ) : subjects.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="p-4 text-center text-muted-foreground">
                      No subjects found.
                    </td>
                  </tr>
                ) : (
                  subjects.map((subject) => (
                    <tr key={subject.id} className="border-b border-input">
                      <td className="p-3 font-mono text-sm">{subject.code}</td>
                      <td className="p-3">{subject.name}</td>
                      <td className="p-3 text-muted-foreground">
                        {subject.description || "—"}
                      </td>
                      <td className="p-3 text-right">
                        <Button variant="outline" size="sm" disabled>
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
          <CardTitle>Create Subject</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleCreate} className="grid gap-4 md:grid-cols-3">
            <div className="space-y-2">
              <Label htmlFor="subject-code">Subject Code</Label>
              <Input
                id="subject-code"
                placeholder="e.g. CS"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="subject-name">Subject Name</Label>
              <Input
                id="subject-name"
                placeholder="e.g. Computer Science"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2 md:col-span-3">
              <Label htmlFor="subject-description">Description</Label>
              <Input
                id="subject-description"
                placeholder="Optional description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>
            <Button type="submit" className="w-auto" disabled={creating}>
              {creating ? "Creating…" : "Create Subject"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

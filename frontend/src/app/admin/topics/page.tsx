"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import {
  createTopic,
  listTopics,
  listSubjects,
  type Subject,
  type Topic,
} from "@/lib/exams";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function TopicsPage() {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [creating, setCreating] = useState(false);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [parentId, setParentId] = useState<string | null>(null);
  const [error, setError] = useState("");

  const loadSubjects = useCallback(async () => {
    try {
      const data = await listSubjects();
      setSubjects(data);
    } catch (err: any) {
      setError(err?.message || "Failed to load subjects");
    }
  }, []);

  const loadTopics = useCallback(async () => {
    if (!selectedSubjectId) return;
    setLoading(true);
    try {
      const data = await listTopics(selectedSubjectId, null);
      setTopics(data);
    } catch (err: any) {
      setError(err?.message || "Failed to load topics");
    } finally {
      setLoading(false);
    }
  }, [selectedSubjectId]);

  useEffect(() => {
    loadSubjects();
  }, [loadSubjects]);

  useEffect(() => {
    loadTopics();
  }, [loadTopics]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (!selectedSubjectId) {
      setError("Please select a subject first");
      return;
    }
    setCreating(true);
    try {
      await createTopic({
        subject_id: selectedSubjectId,
        parent_id: parentId || undefined,
        name,
        description: description || undefined,
      });
      setName("");
      setDescription("");
      setParentId(null);
      await loadTopics();
    } catch (err: any) {
      setError(err?.message || "Failed to create topic");
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Topics</h1>
          <p className="text-muted-foreground">
            Manage hierarchical topics within subjects.
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
          <CardTitle>Select Subject</CardTitle>
          <CardDescription>Choose a subject to view and manage its topics.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {loading ? (
              <span className="text-muted-foreground">Loading subjects…</span>
            ) : subjects.length === 0 ? (
              <span className="text-muted-foreground">No subjects found.</span>
            ) : (
              subjects.map((subject) => (
                <Button
                  key={subject.id}
                  variant={
                    selectedSubjectId === subject.id ? "default" : "outline"
                  }
                  onClick={() => setSelectedSubjectId(subject.id)}
                >
                  {subject.name}
                </Button>
              ))
            )}
          </div>
        </CardContent>
      </Card>

      {selectedSubjectId && (
        <Card>
          <CardHeader>
            <CardTitle>Topics</CardTitle>
            <CardDescription>Topics under the selected subject.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-input text-left text-muted-foreground">
                    <th className="pb-3 font-medium">Name</th>
                    <th className="pb-3 font-medium">Description</th>
                    <th className="pb-3 font-medium">Parent</th>
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
                  ) : topics.length === 0 ? (
                    <tr>
                      <td colSpan={4} className="p-4 text-center text-muted-foreground">
                        No topics found.
                      </td>
                    </tr>
                  ) : (
                    topics.map((topic) => (
                      <tr key={topic.id} className="border-b border-input">
                        <td className="p-3">{topic.name}</td>
                        <td className="p-3 text-muted-foreground">
                          {topic.description || "—"}
                        </td>
                        <td className="p-3 text-muted-foreground">
                          {topic.parent_id ? "Subtopic" : "—"}
                        </td>
                        <td className="p-3 text-right">
                          <Button variant="outline" size="sm" disabled>
                            Edit
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
      )}

      <Card>
        <CardHeader>
          <CardTitle>Create Topic</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleCreate} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="topic-name">Topic Name</Label>
              <Input
                id="topic-name"
                placeholder="e.g. Operating Systems"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                disabled={!selectedSubjectId}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="topic-description">Description</Label>
              <Input
                id="topic-description"
                placeholder="Optional description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                disabled={!selectedSubjectId}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="topic-parent">Parent Topic</Label>
              <Input
                id="topic-parent"
                type="number"
                placeholder="Parent topic ID (optional, leave blank for root)"
                value={parentId || ""}
                onChange={(e) =>
                  setParentId(e.target.value ? e.target.value : null)
                }
                disabled={!selectedSubjectId}
              />
            </div>
            <Button type="submit" className="w-auto" disabled={creating || !selectedSubjectId}>
              {creating ? "Creating…" : "Create Topic"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

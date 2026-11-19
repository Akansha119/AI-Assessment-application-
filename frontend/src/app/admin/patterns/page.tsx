"use client";

import { useEffect, useState, useCallback } from "react";
import {
  listExams,
  type Exam,
} from "@/lib/exams";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function PatternsPage() {
  const [exams, setExams] = useState<Exam[]>([]);
  const [selectedExamId, setSelectedExamId] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadExams = useCallback(async () => {
    setLoading(true);
    try {
      const data = await listExams();
      setExams(data);
    } catch (err: any) {
      setError(err?.message || "Failed to load examinations");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadExams();
  }, [loadExams]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Patterns & Syllabus</h1>
          <p className="text-muted-foreground">
            Configure exam patterns, subject mappings, and syllabus versions.
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
          <CardTitle>Select Examination</CardTitle>
          <CardDescription>Choose an examination to manage its patterns and syllabus.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {loading ? (
              <span className="text-muted-foreground">Loading examinations…</span>
            ) : exams.length === 0 ? (
              <span className="text-muted-foreground">No examinations found. Create one first.</span>
            ) : (
              exams.map((exam) => (
                <Button
                  key={exam.id}
                  variant={
                    selectedExamId === exam.id ? "default" : "outline"
                  }
                  onClick={() => setSelectedExamId(exam.id)}
                >
                  {exam.name}
                </Button>
              ))
            )}
          </div>
        </CardContent>
      </Card>

      {selectedExamId && (
        <>
          <Card>
            <CardHeader>
              <CardTitle>Exam Pattern</CardTitle>
              <CardDescription>Configure the assessment pattern for this examination.</CardDescription>
            </CardHeader>
            <CardContent>
              <form className="grid gap-4 md:grid-cols-4">
                <div className="space-y-2">
                  <Label htmlFor="pattern-name">Pattern Name</Label>
                  <Input
                    id="pattern-name"
                    placeholder="e.g. Standard"
                    disabled
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="pattern-questions">Total Questions</Label>
                  <Input
                    id="pattern-questions"
                    type="number"
                    placeholder="100"
                    disabled
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="pattern-marks">Marks per Correct</Label>
                  <Input
                    id="pattern-marks"
                    type="number"
                    step="0.1"
                    placeholder="2.0"
                    disabled
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="pattern-negative">Negative Marking</Label>
                  <Input
                    id="pattern-negative"
                    type="number"
                    step="0.1"
                    placeholder="0.5"
                    disabled
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="pattern-duration">Duration (minutes)</Label>
                  <Input
                    id="pattern-duration"
                    type="number"
                    placeholder="120"
                    disabled
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="pattern-difficulty">Difficulty Distribution</Label>
                  <Input
                    id="pattern-difficulty"
                    placeholder="JSON"
                    disabled
                  />
                </div>
                <Button type="submit" variant="outline" disabled>
                  Create Pattern
                </Button>
              </form>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Subject Mappings</CardTitle>
              <CardDescription>Subjects mapped to this examination.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button variant="outline" size="sm" disabled>
                Add Subject Mapping
              </Button>
              <div className="border-t border-input pt-4">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-input text-left text-muted-foreground">
                      <th className="pb-3 font-medium">Subject</th>
                      <th className="pb-3 font-medium">Weightage</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td colSpan={2} className="p-4 text-center text-muted-foreground">
                        No subject mappings found.
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Syllabus Versions</CardTitle>
              <CardDescription>Versioned syllabi for this examination.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4 md:grid-cols-3">
                <div className="space-y-2">
                  <Label htmlFor="syll-version">Version</Label>
                  <Input id="syll-version" placeholder="1.0" disabled />
                </div>
                <div className="space-y-2 md:col-span-2">
                  <Label htmlFor="syll-title">Title</Label>
                  <Input id="syll-title" placeholder="Syllabus Title" disabled />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="syll-effective">Effective From</Label>
                  <Input id="syll-effective" placeholder="2024-01-01" disabled />
                </div>
                <Button type="submit" variant="outline" disabled>
                  Create Version
                </Button>
              </div>
              <div className="border-t border-input pt-4">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-input text-left text-muted-foreground">
                      <th className="pb-3 font-medium">Version</th>
                      <th className="pb-3 font-medium">Title</th>
                      <th className="pb-3 font-medium">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td colSpan={3} className="p-4 text-center text-muted-foreground">
                        No syllabus versions found.
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}

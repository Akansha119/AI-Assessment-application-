"use client";

import { useState } from "react";
import { usePathname } from "next/navigation";
import { Link } from "@/components/ui/link";
import { Button } from "@/components/ui/button";
import { removeAccessToken } from "@/lib/api";

const navItems = [
  { name: "Dashboard", href: "/admin", icon: "📊" },
  { name: "Examinations", href: "/admin/exams", icon: "📝" },
  { name: "Subjects", href: "/admin/subjects", icon: "📚" },
  { name: "Topics", href: "/admin/topics", icon: "🌳" },
  { name: "Patterns & Syllabus", href: "/admin/patterns", icon: "⚙️" },
];

export default function AdminLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  const [collapsed, setCollapsed] = useState(false);
  const pathname = usePathname();

  return (
    <div className="flex h-screen bg-background">
      <aside
        className={`fixed inset-y-0 left-0 z-50 w-64 border-r border-input bg-card transition-width duration-200 ${
          collapsed ? "w-20" : "w-64"
        }`}
      >
        <div className="flex items-center justify-between h-12 px-4 border-b border-input">
          <span className="font-semibold tracking-tight">AssessIQ</span>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setCollapsed(!collapsed)}
            aria-label="Toggle sidebar"
          >
            {collapsed ? "▶" : "◀"}
          </Button>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          {navItems.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.name}
                asChild
                href={item.href}
                className="block"
              >
                <a
                  className={`flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    active
                      ? "bg-primary text-primary-foreground"
                      : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                  }`}
                >
                  <span className="w-8 text-center">{item.icon}</span>
                  {!collapsed && item.name}
                </a>
              </Link>
            );
          })}
        </nav>
        <div className="p-4 border-t border-input">
          <Button
            variant="destructive"
            onClick={() => {
              removeAccessToken();
              window.location.href = "/login";
            }}
            className="w-full"
          >
            Sign out
          </Button>
        </div>
      </aside>
      <div className="flex-1 overflow-hidden">
        <main className="flex-1 p-6 overflow-y-auto">{children}</main>
      </div>
    </div>
  );
}

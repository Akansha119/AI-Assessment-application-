"use client";

export const dynamic = "force-dynamic";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getAccessToken } from "@/lib/api";

export default function Home() {
  const [checked, setChecked] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const token = getAccessToken();
    setChecked(true);
    if (token) {
      router.push("/dashboard");
    } else {
      router.push("/login");
    }
  }, [router]);

  if (!checked) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <span>Loading...</span>
      </div>
    );
  }
  return null;
}

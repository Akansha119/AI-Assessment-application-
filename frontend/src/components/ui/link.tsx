"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

interface LinkProps
  extends React.AnchorHTMLAttributes<HTMLAnchorElement> {
  asChild?: boolean;
}

const Link = React.forwardRef<HTMLAnchorElement, LinkProps>(
  ({ className, asChild = false, ...props }, ref) => {
    const Comp = asChild ? React.Fragment : ("a" as const);
    return (
      <Comp
        ref={ref}
        className={cn(
          "text-primary font-medium transition-colors hover:underline",
          className
        )}
        {...props}
      />
    );
  }
);
Link.displayName = "Link";

export { Link };

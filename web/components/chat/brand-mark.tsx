import { APP_CONFIG } from "@/lib/config";
import { cn } from "@/lib/utils";

/** The app's logo: the first letter of its name on the accent colour. */
export function BrandMark({ className }: { className?: string }) {
  return (
    <span
      aria-hidden
      className={cn(
        "grid shrink-0 place-items-center rounded-lg bg-primary font-semibold text-primary-foreground select-none",
        className,
      )}
    >
      {APP_CONFIG.appName.charAt(0).toUpperCase()}
    </span>
  );
}

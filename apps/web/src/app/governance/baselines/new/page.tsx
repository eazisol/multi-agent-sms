import { AppShell } from "@/components/app-shell";
import { BaselineCreatePage } from "@/components/baseline-create-page";

export default function Page() {
  return (
    <AppShell title="New baseline">
      <BaselineCreatePage />
    </AppShell>
  );
}

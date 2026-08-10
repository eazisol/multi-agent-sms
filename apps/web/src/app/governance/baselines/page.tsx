import { AppShell } from "@/components/app-shell";
import { BaselineListPage } from "@/components/baseline-list-page";

export default function Page() {
  return (
    <AppShell title="Source baselines">
      <BaselineListPage />
    </AppShell>
  );
}

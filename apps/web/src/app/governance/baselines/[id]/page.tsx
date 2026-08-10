import { AppShell } from "@/components/app-shell";
import { BaselineDetailPage } from "@/components/baseline-detail-page";

export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return (
    <AppShell title="Baseline detail">
      <BaselineDetailPage baselineId={id} />
    </AppShell>
  );
}

type LoginPageProps = {
  searchParams: Promise<{ returnTo?: string }>;
};

export default async function LoginPage({ searchParams }: LoginPageProps) {
  const params = await searchParams;
  const requested = params.returnTo;
  const returnTo =
    requested && requested.startsWith("/") && !requested.startsWith("//") ? requested : "/";
  const loginHref = `/auth/login?${new URLSearchParams({ returnTo }).toString()}`;

  return (
    <main className="grid min-h-screen place-items-center bg-[var(--background)] p-6">
      <section className="w-full max-w-md rounded-2xl border bg-[var(--surface)] p-8 shadow-sm">
        <p className="text-xs font-semibold uppercase tracking-wider text-[var(--accent)]">
          MASMS
        </p>
        <h1 className="mt-3 text-2xl font-semibold">Sign in to your workspace</h1>
        <p className="mt-2 text-sm text-[var(--muted)]">
          Authentication is handled by the configured Auth0 development tenant.
        </p>
        <a
          className="mt-6 block rounded-lg bg-[var(--accent)] px-4 py-3 text-center text-sm font-semibold text-white"
          href={loginHref}
        >
          Continue with Auth0
        </a>
      </section>
    </main>
  );
}

import { expect, test } from "@playwright/test";

test.describe("local workspace smoke", () => {
  test("loads the shell and primary desks without server errors", async ({ page }) => {
    const serverErrors: string[] = [];
    page.on("response", (response) => {
      if (response.url().includes("/api/") && response.status() >= 500) {
        serverErrors.push(`${response.status()} ${response.url()}`);
      }
    });

    await page.goto("/");
    await expect(page.getByRole("navigation", { name: "Primary" })).toBeVisible();
    await expect(page.getByLabel("UI role variant")).toBeVisible();

    await page.goto("/clients");
    await expect(page.getByRole("heading", { name: "Clients" })).toBeVisible();

    await page.goto("/tickets");
    await expect(page.getByRole("heading", { name: "Tickets" })).toBeVisible();

    expect(serverErrors).toEqual([]);
  });

  test("exposes the Auth0 sign-in entry page", async ({ page }) => {
    await page.goto("/login");
    await expect(
      page.getByRole("heading", { name: "Sign in to your workspace" }),
    ).toBeVisible();
    await expect(page.getByRole("link", { name: "Continue with Auth0" })).toHaveAttribute(
      "href",
      /\/auth\/login/,
    );
  });
});

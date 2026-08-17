import { expect, test } from "@playwright/test";

test("uses authenticated identity instead of the local role stub", async ({ page }) => {
  test.skip(
    process.env.PLAYWRIGHT_AUTH0_TEST !== "true",
    "Requires an approved Auth0 sandbox session",
  );

  await page.goto("/");
  await expect(page.getByRole("link", { name: "Logout" })).toBeVisible();
  await expect(page.getByLabel("UI role variant")).toHaveCount(0);
});

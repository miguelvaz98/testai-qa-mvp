import { test, expect } from '@playwright/test';

test.describe('Test Generator Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://127.0.0.1:3000');
  });

  test('should have textarea for code input', async ({ page }) => {
    const textarea = page.locator('textarea');
    await expect(textarea).toBeVisible();
  });

  test('should have framework select dropdown', async ({ page }) => {
    const select = page.locator('select');
    await expect(select).toBeVisible();
  });

  test('should have Generar Tests button', async ({ page }) => {
    const button = page.locator('button', { hasText: 'Generar Tests' });
    await expect(button).toBeVisible();
  });

  test('should have hidden pre element for results', async ({ page }) => {
    const preElement = page.locator('pre');
    await expect(preElement).toBeHidden();
  });

  test('should send POST request and display results on button click', async ({ page }) => {
    const testCode = 'function add(a, b) { return a + b; }';
    const textarea = page.locator('textarea');
    const select = page.locator('select');
    const button = page.locator('button', { hasText: 'Generar Tests' });
    const preElement = page.locator('pre');

    // Fill textarea with code
    await textarea.fill(testCode);

    // Select framework
    await select.selectOption('playwright');

    // Mock the API response
    await page.route('http://127.0.0.1:8000/api/generate', (route) => {
      route.abort('blockedbyresponse');
    });

    await page.route('http://127.0.0.1:8000/api/generate', (route) => {
      route.continue({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          tests: 'test("should add numbers", () => { expect(add(1, 2)).toBe(3); });',
        }),
      });
    });

    // Click the button
    await button.click();

    // Wait for the pre element to become visible
    await expect(preElement).toBeVisible({ timeout: 5000 });

    // Check that the result contains generated test code
    await expect(preElement).toContainText('test');
  });

  test('should allow changing framework selection', async ({ page }) => {
    const select = page.locator('select');

    // Check available options
    const optionValues = ['playwright', 'cypress', 'jest'];

    for (const value of optionValues) {
      await select.selectOption(value);
      const selectedValue = await select.inputValue();
      expect(selectedValue).toBe(value);
    }
  });

  test('should handle empty textarea gracefully', async ({ page }) => {
    const textarea = page.locator('textarea');
    const button = page.locator('button', { hasText: 'Generar Tests' });

    // Ensure textarea is empty
    await textarea.fill('');

    // Try to generate tests with empty code
    await button.click();

    // The page should still be responsive
    await expect(textarea).toBeVisible();
  });
});
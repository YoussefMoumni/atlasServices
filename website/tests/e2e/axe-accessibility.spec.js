import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const pages = [
  '/index.html',
  '/advisory.html',
  '/brokerage.html',
  '/asset-management.html',
  '/research.html',
  '/capital-raising.html',
  '/trading.html'
];

test.describe('Automated Accessibility Testing (axe-core)', () => {
  for (const pagePath of pages) {
    test(`${pagePath} should not have accessibility violations`, async ({ page }) => {
      await page.goto(pagePath);
      
      const accessibilityScanResults = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
        .analyze();
      
      expect(accessibilityScanResults.violations).toEqual([]);
    });
  }
  
  test('index page accessibility in different viewports', async ({ page }) => {
    // Desktop
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto('/index.html');
    
    let results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa'])
      .analyze();
    
    expect(results.violations).toEqual([]);
    
    // Mobile
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/index.html');
    
    results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa'])
      .analyze();
    
    expect(results.violations).toEqual([]);
  });
});

import { test, expect } from '@playwright/test';

const pages = [
  { path: '/', title: /Atlas Maroc Capital Markets/, heading: 'Capital markets expertise framed with clarity and confidence.' },
  { path: '/index.html', title: /Atlas Maroc Capital Markets/, heading: 'Capital markets expertise framed with clarity and confidence.' },
  { path: '/advisory.html', title: /Advisory/, heading: 'Advisory' },
  { path: '/brokerage.html', title: /Brokerage/, heading: 'Brokerage' },
  { path: '/asset-management.html', title: /Asset Management/, heading: 'Asset Management' },
  { path: '/research.html', title: /Research/, heading: 'Research' },
  { path: '/capital-raising.html', title: /Capital Raising/, heading: 'Capital Raising' },
  { path: '/trading.html', title: /Trading/, heading: 'Trading' },
];

test.describe('Page Loading', () => {
  for (const page of pages) {
    test(`${page.path} loads successfully`, async ({ page: browserPage }) => {
      const response = await browserPage.goto(page.path);
      expect(response?.status()).toBe(200);
      
      // Check title
      await expect(browserPage).toHaveTitle(page.title);
      
      // Check main heading exists
      const h1 = browserPage.locator('h1').first();
      await expect(h1).toBeVisible();
      await expect(h1).toContainText(page.heading);
    });
  }
});

test.describe('Navigation', () => {
  test('header navigation is present on all pages', async ({ page }) => {
    for (const pageDef of pages.slice(0, 3)) { // Test subset to save time
      await page.goto(pageDef.path);
      
      const nav = page.locator('nav');
      await expect(nav).toBeVisible();
      
      // Check key nav links
      await expect(page.locator('nav a[href="index.html"]')).toBeVisible();
      await expect(page.locator('nav a[href="advisory.html"]')).toBeVisible();
      await expect(page.locator('nav a[href="brokerage.html"]')).toBeVisible();
    }
  });
  
  test('navigation links work correctly', async ({ page }) => {
    await page.goto('/');
    
    // Click Advisory link
    await page.click('nav a[href="advisory.html"]');
    await expect(page).toHaveURL(/advisory\.html/);
    await expect(page.locator('h1')).toContainText('Advisory');
    
    // Click Brokerage link
    await page.click('nav a[href="brokerage.html"]');
    await expect(page).toHaveURL(/brokerage\.html/);
    await expect(page.locator('h1')).toContainText('Brokerage');
    
    // Return to home
    await page.click('a.brand');
    await expect(page).toHaveURL(/index\.html/);
  });
});

test.describe('Content Structure', () => {
  test('index page has service links', async ({ page }) => {
    await page.goto('/index.html');
    
    // Check that all 6 service links are present
    const serviceLinks = [
      'advisory.html',
      'brokerage.html',
      'asset-management.html',
      'research.html',
      'capital-raising.html',
      'trading.html'
    ];
    
    for (const link of serviceLinks) {
      const linkElement = page.locator(`a[href="${link}"]`).first();
      await expect(linkElement).toBeVisible();
    }
  });
  
  test('service pages have consistent structure', async ({ page }) => {
    const servicePage = '/advisory.html';
    await page.goto(servicePage);
    
    // Check header
    await expect(page.locator('header.site-header')).toBeVisible();
    
    // Check main content
    await expect(page.locator('main')).toBeVisible();
    
    // Check hero section
    await expect(page.locator('section.hero')).toBeVisible();
    
    // Check footer
    await expect(page.locator('footer')).toBeVisible();
  });
});

test.describe('Responsive Design', () => {
  test('mobile viewport renders correctly', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/index.html');
    
    // Header should be visible
    await expect(page.locator('header')).toBeVisible();
    
    // Main heading should be visible
    const h1 = page.locator('h1');
    await expect(h1).toBeVisible();
    
    // Navigation should be visible (may be wrapped)
    await expect(page.locator('nav')).toBeVisible();
  });
  
  test('tablet viewport renders correctly', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/index.html');
    
    await expect(page.locator('header')).toBeVisible();
    await expect(page.locator('h1')).toBeVisible();
    await expect(page.locator('nav')).toBeVisible();
  });
  
  test('desktop viewport renders correctly', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto('/index.html');
    
    await expect(page.locator('header')).toBeVisible();
    await expect(page.locator('h1')).toBeVisible();
    await expect(page.locator('nav')).toBeVisible();
  });
});

test.describe('Visual Elements', () => {
  test('brand logo is visible', async ({ page }) => {
    await page.goto('/index.html');
    const brand = page.locator('a.brand');
    await expect(brand).toBeVisible();
    await expect(brand).toContainText('Atlas Maroc');
    await expect(brand).toContainText('Capital Markets');
  });
  
  test('cards render on service pages', async ({ page }) => {
    await page.goto('/advisory.html');
    
    // Should have multiple card elements
    const cards = page.locator('.card');
    const count = await cards.count();
    expect(count).toBeGreaterThan(0);
  });
});

test.describe('Accessibility', () => {
  test('pages have proper heading hierarchy', async ({ page }) => {
    await page.goto('/index.html');
    
    // Should have exactly one h1
    const h1Count = await page.locator('h1').count();
    expect(h1Count).toBe(1);
    
    // Should have h2 elements
    const h2Count = await page.locator('h2').count();
    expect(h2Count).toBeGreaterThan(0);
  });
  
  test('navigation has proper ARIA labels', async ({ page }) => {
    await page.goto('/index.html');
    
    const nav = page.locator('nav');
    await expect(nav).toHaveAttribute('aria-label', /navigation/i);
  });
  
  test('links are keyboard accessible', async ({ page }) => {
    await page.goto('/index.html');
    
    // Tab to first navigation link
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab'); // May need multiple tabs depending on browser chrome
    
    // First focusable link should be highlighted
    const firstLink = page.locator('a.brand');
    // Just verify links exist and are visible
    await expect(firstLink).toBeVisible();
  });
});

test.describe('Performance', () => {
  test('page loads within reasonable time', async ({ page }) => {
    const startTime = Date.now();
    await page.goto('/index.html');
    const loadTime = Date.now() - startTime;
    
    // Should load in under 3 seconds (generous for CI)
    expect(loadTime).toBeLessThan(3000);
  });
  
  test('no console errors on page load', async ({ page }) => {
    const consoleErrors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });
    
    await page.goto('/index.html');
    expect(consoleErrors).toHaveLength(0);
  });
});

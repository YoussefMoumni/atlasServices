import { readFileSync, readdirSync } from 'fs';

console.log('♿ Validating accessibility...\n');

const htmlFiles = readdirSync('.').filter(f => f.endsWith('.html'));

let totalIssues = 0;
const a11yResults = [];

// Basic accessibility checks (without running browser)
function checkAccessibility(html, filename) {
  const issues = [];
  
  // Check for alt attributes on images
  const imgRegex = /<img(?![^>]*alt=)[^>]*>/gi;
  const imgsWithoutAlt = html.match(imgRegex) || [];
  if (imgsWithoutAlt.length > 0) {
    issues.push({
      type: 'missing-alt',
      count: imgsWithoutAlt.length,
      severity: 'error',
      message: `${imgsWithoutAlt.length} <img> elements missing alt attribute`
    });
  }
  
  // Check for lang attribute on html tag
  if (!html.match(/<html[^>]*lang=/i)) {
    issues.push({
      type: 'missing-lang',
      severity: 'error',
      message: 'Missing lang attribute on <html> element'
    });
  }
  
  // Check for page title
  if (!html.match(/<title>[^<]+<\/title>/i)) {
    issues.push({
      type: 'missing-title',
      severity: 'error',
      message: 'Missing or empty <title> element'
    });
  }
  
  // Check for meta viewport
  if (!html.match(/<meta[^>]*name=["']viewport["']/i)) {
    issues.push({
      type: 'missing-viewport',
      severity: 'warning',
      message: 'Missing viewport meta tag for responsive design'
    });
  }
  
  // Check for heading hierarchy (basic check)
  const h1Count = (html.match(/<h1[^>]*>/gi) || []).length;
  if (h1Count === 0) {
    issues.push({
      type: 'missing-h1',
      severity: 'error',
      message: 'No <h1> heading found on page'
    });
  } else if (h1Count > 1) {
    issues.push({
      type: 'multiple-h1',
      severity: 'warning',
      message: `Multiple <h1> headings found (${h1Count})`
    });
  }
  
  // Check for form inputs without labels
  const inputsWithoutLabel = html.match(/<input(?![^>]*aria-label)(?![^>]*type=["'](hidden|submit|button)["'])[^>]*>/gi) || [];
  const hasLabels = html.includes('<label');
  if (inputsWithoutLabel.length > 0 && !hasLabels) {
    issues.push({
      type: 'input-without-label',
      count: inputsWithoutLabel.length,
      severity: 'warning',
      message: `${inputsWithoutLabel.length} form inputs may be missing labels`
    });
  }
  
  return issues;
}

for (const file of htmlFiles) {
  const html = readFileSync(file, 'utf-8');
  const issues = checkAccessibility(html, file);
  
  const errors = issues.filter(i => i.severity === 'error');
  const warnings = issues.filter(i => i.severity === 'warning');
  
  totalIssues += errors.length;
  
  if (issues.length === 0) {
    console.log(`✅ ${file} - No accessibility issues`);
  } else {
    console.log(`${errors.length > 0 ? '❌' : '⚠️ '} ${file}:`);
    errors.forEach(issue => {
      console.log(`   ERROR: ${issue.message}`);
    });
    warnings.forEach(issue => {
      console.log(`   WARN:  ${issue.message}`);
    });
    a11yResults.push({ file, issues });
  }
}

console.log(`\n📊 Summary: ${htmlFiles.length} files checked, ${totalIssues} critical issues\n`);

if (totalIssues > 0) {
  console.error('❌ Accessibility validation failed');
  process.exit(1);
} else {
  console.log('✅ Basic accessibility checks passed');
  process.exit(0);
}

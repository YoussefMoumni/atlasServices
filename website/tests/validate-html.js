import { HtmlValidate } from 'html-validate';
import { readFileSync, readdirSync } from 'fs';
import { join } from 'path';

const validator = new HtmlValidate();
const htmlFiles = readdirSync('.').filter(f => f.endsWith('.html'));

console.log('🔍 Validating HTML files...\n');

let totalErrors = 0;
let totalWarnings = 0;
const results = [];

for (const file of htmlFiles) {
  const html = readFileSync(file, 'utf-8');
  const report = await validator.validateString(html, file);
  
  const errors = report.results[0]?.messages.filter(m => m.severity === 2) || [];
  const warnings = report.results[0]?.messages.filter(m => m.severity === 1) || [];
  
  totalErrors += errors.length;
  totalWarnings += warnings.length;
  
  results.push({
    file,
    valid: report.valid,
    errors,
    warnings
  });
  
  if (report.valid) {
    console.log(`✅ ${file} - Valid`);
  } else {
    console.log(`❌ ${file} - ${errors.length} errors, ${warnings.length} warnings`);
    
    errors.forEach(msg => {
      console.log(`   ERROR [${msg.line}:${msg.column}] ${msg.message}`);
    });
    
    warnings.forEach(msg => {
      console.log(`   WARN  [${msg.line}:${msg.column}] ${msg.message}`);
    });
  }
}

console.log(`\n📊 Summary: ${htmlFiles.length} files, ${totalErrors} errors, ${totalWarnings} warnings\n`);

if (totalErrors > 0) {
  console.error('❌ HTML validation failed');
  process.exit(1);
} else {
  console.log('✅ All HTML files are valid');
  process.exit(0);
}

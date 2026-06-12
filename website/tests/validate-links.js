import { readFileSync, readdirSync } from 'fs';
import { join } from 'path';

console.log('🔗 Validating internal links...\n');

const htmlFiles = readdirSync('.').filter(f => f.endsWith('.html'));
const allFiles = new Set(htmlFiles);

let totalLinks = 0;
let brokenLinks = 0;
const linkResults = [];

// Extract href attributes from HTML
function extractLinks(html) {
  const linkRegex = /href=["']([^"']+)["']/g;
  const links = [];
  let match;
  
  while ((match = linkRegex.exec(html)) !== null) {
    links.push(match[1]);
  }
  
  return links;
}

for (const file of htmlFiles) {
  const html = readFileSync(file, 'utf-8');
  const links = extractLinks(html);
  
  const internalLinks = links.filter(link => 
    !link.startsWith('http://') && 
    !link.startsWith('https://') && 
    !link.startsWith('#') &&
    !link.startsWith('mailto:')
  );
  
  totalLinks += internalLinks.length;
  
  const broken = internalLinks.filter(link => {
    // Remove hash fragments
    const cleanLink = link.split('#')[0];
    if (!cleanLink) return false; // Pure hash link is OK
    
    return !allFiles.has(cleanLink);
  });
  
  brokenLinks += broken.length;
  
  if (broken.length > 0) {
    console.log(`❌ ${file}:`);
    broken.forEach(link => {
      console.log(`   Missing: ${link}`);
    });
    linkResults.push({ file, broken });
  } else if (internalLinks.length > 0) {
    console.log(`✅ ${file} - ${internalLinks.length} internal links OK`);
  }
}

console.log(`\n📊 Summary: ${totalLinks} internal links checked, ${brokenLinks} broken\n`);

if (brokenLinks > 0) {
  console.error('❌ Link validation failed');
  process.exit(1);
} else {
  console.log('✅ All internal links are valid');
  process.exit(0);
}

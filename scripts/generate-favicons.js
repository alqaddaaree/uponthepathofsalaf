import sharp from 'sharp';
import fs from 'fs';
import path from 'path';

const __dirname = path.dirname(new URL(import.meta.url).pathname);
const input = path.join(__dirname, '../public/logo.jpg');
const outputDir = path.join(__dirname, '../public');

if (!fs.existsSync(input)) {
  console.error('❌ logo.jpg not found in public/');
  process.exit(1);
}

const sizes = [16, 32, 64, 128, 192, 512];
sizes.forEach(size => {
  sharp(input)
    .resize(size, size)
    .toFile(path.join(outputDir, `icon-${size}x${size}.png`))
    .then(() => console.log(`✅ Generated icon-${size}x${size}.png`))
    .catch(err => console.error(`❌ Failed icon-${size}x${size}:`, err));
});

// Favicon (32x32 as PNG)
sharp(input)
  .resize(32, 32)
  .toFile(path.join(outputDir, 'favicon.png'))
  .then(() => console.log('✅ Generated favicon.png'))
  .catch(err => console.error('❌ favicon.png:', err));

// Apple touch icon (180x180)
sharp(input)
  .resize(180, 180)
  .toFile(path.join(outputDir, 'apple-touch-icon.png'))
  .then(() => console.log('✅ Generated apple-touch-icon.png'))
  .catch(err => console.error('❌ apple-touch-icon:', err));

console.log('🎨 Favicon generation started. Check public/ for generated files.');

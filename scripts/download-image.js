import https from 'https';
import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Get command line arguments
const args = process.argv.slice(2);
if (args.length < 2) {
  console.error('Usage: node download-image.js "<keyword>" "<output-path>"');
  process.exit(1);
}

const keyword = args[0];
const outputPath = args[1];
const accessKey = process.env.UNSPLASH_ACCESS_KEY;

if (!accessKey) {
  console.error('Error: UNSPLASH_ACCESS_KEY environment variable is not set');
  process.exit(1);
}

// Ensure output directory exists
const outputDir = path.dirname(outputPath);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// Search for photos on Unsplash
const searchUrl = `https://api.unsplash.com/search/photos?query=${encodeURIComponent(keyword)}&per_page=1&orientation=landscape`;

console.log(`Searching Unsplash for: ${keyword}`);

https.get(searchUrl, {
  headers: {
    'Authorization': `Client-ID ${accessKey}`
  }
}, (res) => {
  let data = '';

  res.on('data', (chunk) => {
    data += chunk;
  });

  res.on('end', () => {
    try {
      const json = JSON.parse(data);

      if (json.results && json.results.length > 0) {
        const photo = json.results[0];
        const imageUrl = photo.urls.regular;

        console.log(`Found image by: ${photo.user.name}`);
        console.log(`Downloading from: ${imageUrl}`);

        // Download the image
        const imageProtocol = imageUrl.startsWith('https') ? https : http;
        imageProtocol.get(imageUrl, (imgRes) => {
          const fileStream = fs.createWriteStream(outputPath);
          imgRes.pipe(fileStream);

          fileStream.on('finish', () => {
            fileStream.close();
            console.log(`Image saved to: ${outputPath}`);
          });
        }).on('error', (err) => {
          console.error('Error downloading image:', err.message);
          process.exit(1);
        });
      } else {
        console.error('No images found for the keyword');
        process.exit(1);
      }
    } catch (err) {
      console.error('Error parsing Unsplash response:', err.message);
      process.exit(1);
    }
  });
}).on('error', (err) => {
  console.error('Error searching Unsplash:', err.message);
  process.exit(1);
});
